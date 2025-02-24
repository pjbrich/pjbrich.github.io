;; Will fill an AutoCAD polyline with a repeating block pattern and explode each block immediately after placement
;; 02/10/2025
;; Created by Benjamin Richards
(defun c:PopulatePolylineWithPattern (/ pline blockName interval dist pt param tangent dx dy rotationAngle insertedBlock)
  ;; Prompt the user to select a polyline
  (setq pline (car (entsel "\nSelect a polyline: ")))
  
  ;; Check if the selected entity is a polyline
  (if (and pline
           (setq plineData (entget pline))
           (eq (cdr (assoc 0 plineData)) "LWPOLYLINE"))
    (progn
      ;; Prompt the user for the block name
      (setq blockName "GPL") ;; Replace with your block name
      
      ;; Prompt the user for the interval distance
      (setq interval 136) ;; Set your desired interval
      
      ;; Initialize the distance along the polyline
      (setq dist 0.0)
      
      ;; Loop to insert blocks along the polyline
      (while (< dist (vlax-curve-getDistAtParam pline (vlax-curve-getEndParam pline)))
        ;; Get the point at the current distance
        (setq pt (vlax-curve-getPointAtDist pline dist))
        
        ;; Calculate the tangent vector at this point
        (setq param (vlax-curve-getParamAtDist pline dist))
        (setq tangent (vlax-curve-getFirstDeriv pline param))
        
        ;; Extract X and Y components of the tangent vector
        (setq dx (car tangent))
        (setq dy (cadr tangent))
        
        ;; Calculate the rotation angle in degrees using atan2
        ;; atan returns radians, so we convert to degrees with (* 180.0 (/ pi))
        (setq rotationAngle (* 180.0 (/ (atan dy dx) pi)))
        
        ;; Insert and rotate the block to align with the polyline's direction
        (command "_.insert" blockName pt "" "" rotationAngle)
        
        ;; Select and explode the last inserted block using entlast
        (setq insertedBlock (entlast)) ; Get the last created entity
        (if insertedBlock
          (command "_.explode" insertedBlock) ; Explode it immediately after insertion
        )
        
        ;; Increment the distance by the interval
        (setq dist (+ dist interval))
      )
      
      (princ "\nBlocks inserted, aligned, and exploded along the polyline.")
    )
    (princ "\nThe selected entity is not a polyline.")
  )
  (princ)
)
