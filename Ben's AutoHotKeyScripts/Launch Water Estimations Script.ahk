#Requires AutoHotkey v2.0

!w::
{
    static presses := 0
    presses++
    SetTimer(ResetPresses, -300)

    if (presses = 2)
    {
        Run("C:\Users\Exlterra CAD 02\Documents\GitHub\pjbrich.github.io\python scripts\waterEstimations.pyw")
        presses := 0
    }
}

ResetPresses()
{
    presses := 0
}
