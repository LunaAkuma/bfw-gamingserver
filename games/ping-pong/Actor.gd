extends CharacterBody2D
class_name Actor

@export var speed: = 150.0
@export var paddle_width: = 10.0
@export var paddle_height: = 50.0
@export var color: Color = Color.WHITE

@onready var screen_size: = get_viewport_rect().size
var paddle_center

func _draw():
	draw_rect(Rect2(-paddle_width/2, -paddle_center, paddle_width, paddle_height), color)
	

func start_position(pos: Vector2) -> void:
	position = pos	
