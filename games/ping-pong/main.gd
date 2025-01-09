extends Control

@onready var screen_size: = get_viewport_rect().size
@onready var pad1: = get_node("Player1/Player")
@onready var pad2: = get_node("Player2/Player2")
@onready var ball: = get_node("Ball")
@onready var startpos1: = get_node("Player1/Mark2D")
@onready var startpos2: = get_node("Player2/Mark2D")
@onready var interface: = get_node("HUD")

const dash_width: = 8.0
const dash_distance: = 10.0
const border_wall_height: = 15.0

 
var half_screen: Vector2

func _ready():
	half_screen = Vector2(screen_size.x/2, screen_size.y/2)
	Reset_Game()

func _draw():
	
	draw_dashed_line(Vector2(half_screen.x, 0), Vector2(half_screen.x, screen_size.y), Color.WHITE, dash_width, dash_distance)
	
	draw_line(Vector2.ZERO, Vector2(screen_size.x, 0), Color.YELLOW, border_wall_height)
	
	draw_line(Vector2(0, screen_size.y), Vector2(screen_size.x, screen_size.y), Color.YELLOW, border_wall_height)
	
func ready_position():
	pad1.start_position(startpos1.position)
	pad2.start_position(startpos2.position)
	ball.start_position(half_screen)

	
	


func _on_ball_gameover(user_win: bool):
	interface.find_winner(user_win)
	Reset_Game()


func Reset_Game() -> void:
	ready_position()
	ball.direction()
