; The notes and envelope length (?) from zeldasource.

SONG_END = $00
C6		 = $02
Db_3	 = $04
Gb_5	 = $06
REST	 = $08 ; This is a bit of a misnomer, it seems like a "continue", not a rest note.
D_3		 = $0A
Eb_3	 = $0C
E_3		 = $0E
F_3		 = $10
Gb_3	 = $12
G_3		 = $14
Ab_3	 = $16
A_3		 = $18
Bb_3	 = $1A
B_3		 = $1C
C_4		 = $1E
Db_4	 = $20
D_4		 = $22
Eb_4	 = $24
E_4		 = $26
F_4		 = $28
Gb_4	 = $2A
G_4		 = $2C
Ab_4	 = $2E
A_4		 = $30
Bb_4	 = $32
B_4		 = $34
C_5		 = $36
Db_5	 = $38
D_5		 = $3A
Eb_5	 = $3C
E_5		 = $3E
F_5		 = $40
G_5		 = $42
Ab_5	 = $44
Bb_5	 = $46
A_5		 = $48
B_5		 = $4A
E_6		 = $4C
Db_6	 = $4E
D_6		 = $50
Eb_6	 = $52
F_6		 = $54
G_6		 = $56
Ab_6	 = $58
A_6		 = $5A
B_6		 = $5C
C_7		 = $5E
Ab_7	 = $60
E_2		 = $62
F_2		 = $64
Gb_2	 = $66
Ab_2	 = $68
A_2		 = $6A
Bb_2	 = $6C
B_2		 = $6E
C_3		 = $70

; Usage: .byte NOTE_LENGTH|10 for 10 frames
NOTE_LENGTH         = $80

; Usage: .byte VOLUME|15 for max value, .byte VOLUME|0 for silence.
; This only works for Tune0s
VOLUME  = $90

; Resets sound for any Tune request
ResetSound = 0

; Stored in the A register when setting Tune0Request
PlayRupeeSound        = 1 << 0 ; $01
PlayHarmedSound       = 1 << 1 ; $02
PlayMagicShotSound    = 1 << 2 ; $04
PlayKeyPickupSound    = 1 << 3 ; $08
PlayHeartPickupSound  = 1 << 4 ; $10
PlayBombPlacedSound   = 1 << 5 ; $20
PlayLowHealthSound    = 1 << 6 ; $40
PlaySilence           = 1 << 7 ; $80

; Stored in the A register when setting Tune1Request
PlayRupeePickupSound  = 1 << 0 ; $01
PlayItemAppearsSound  = 1 << 1 ; $02
PlaySecretFoundSound  = 1 << 2 ; $04
PlayItemPickupSound   = 1 << 3 ; $08
PlayRecorderSound     = 1 << 4 ; $10
PlayEnemyDeathSound   = 1 << 5 ; $20
PlayGameOverMusic     = 1 << 6 ; $40
PlayDeathSound        = 1 << 7 ; $80
