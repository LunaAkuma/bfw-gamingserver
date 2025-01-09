extends CanvasLayer

@onready var score1: = get_node("SCORE1")
@onready var score2: = get_node("SCORE2")

var player1_score: =0
var player2_score: =0

func _ready():
	_update_score()

func find_winner(value: bool) -> void:
	if value: player1_score += 1
	else: player2_score += 1
	_update_score()

func _update_score() -> void:
	score1.text = "%s" % player1_score
	score2.text = "%s" % player2_score
