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
					'move relative (VAL(S11),VAL(S12),VAL(S13))
				CASE "MA"
					'move absolute (VAL(S11),VAL(S12),VAL(S13))
				CASE "MJR"
					'Move joint relative (VAL(S11),VAL(S12))
				CASE "MJA"
					'Move joint absolute (VAL(S11),VAL(S12))
				CASE "SS"
					'Set speed (VAL(S11))
				CASE "GS"
					'Get speed
				CASE "GP"
					'Get position
				CASE "GPJ"
					'Get joint position
				CASE "MP"
					'Move to point
					MOVE P, VAL(S11)
			END SELECT
			PRINT #4, "DONE"
			COM_STATE #4, I1
			IF I1 = -1 THEN
				EXIT DO
		LOOP
	END IF
LOOP

GIVEARM


END