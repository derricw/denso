'!TITLE "<Title>"
PROGRAM STARTCOM

TAKEARM 0

'Wait for connection
DO WHILE 1
	COM_STATE #4, I1
	IF I1 = -1 THEN    'NOT CONNECTED
		COM_ENCOM #4
		FLUSH #4
		DELAY 1
	ELSE
		DO WHILE 1
			FLUSH #4
			INPUT #4, S10,S11,S12,S13
			SELECT CASE S10
				CASE "MR"
					'move relative (X,Y,Z)
					DRAW P, (VAL(S11),VAL(S12),VAL(S13)), NEXT
					PRINT #4, "DONE"
				CASE "MJA"
					'move absolute (joint, degrees)
					DRIVEA, (VAL(S11),VAL(S12)), NEXT
				CASE "MJR"
					'Move joint relative (VAL(S11),VAL(S12))
				CASE "SS"
					'Set speed (VAL(S11))
				CASE "GS"
					'Get speed
				CASE "GPJ"
					'Get joint position
					DIM LJ1 AS JOINT
					LJ1 = CURJNT
					PRINT #4 LJ1
				CASE "MP"
					'Move to point
			END SELECT
			PRINT #4, "DONE"
			COM_STATE #4, I1
			IF I1 = -1 THEN
				EXIT DO
			END IF
		LOOP
	END IF
LOOP

GIVEARM


END