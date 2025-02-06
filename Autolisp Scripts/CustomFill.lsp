(defun c:PopulatePolylineWithBlock (/ pline blockName interval dist pt param)
  ;; Prompt the user to select a polyline
  (setq pline (car (entsel "\nSelect a polyline: ")))
  
  ;; Check if the selected entity is a polyline
  (if (and pline
           (setq plineData (entget pline))
           (eq (cdr (assoc 0 plineData)) "LWPOLYLINE"))
    (progn
      ;; Prompt the user for the block name
      (setq blockName (getstring "\nEnter the block name: "))
      
      ;; Prompt the user for the interval distance
      (setq interval (getdist "\nEnter the interval distance: "))
      
      ;; Initialize the distance along the polyline
      (setq dist 0.0)
      
      ;; Loop to insert blocks along the polyline
      (while (< dist (vlax-curve-getDistAtParam pline (vlax-curve-getEndParam pline)))
        ;; Get the point at the current distance
        (setq pt (vlax-curve-getPointAtDist pline dist))
        
        ;; Insert the block at the point
        (command "_.insert" blockName pt "" "" "")
        
        ;; Increment the distance by the interval
        (setq dist (+ dist interval))
      )
      (princ "\nBlocks inserted along the polyline.")
    )
    (princ "\nThe selected entity is not a polyline.")
  )
  (princ)
)