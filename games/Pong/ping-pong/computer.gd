extends Actor

@onready var collision_shape: = get_node("CollisionShape2D")

@export var ball: CharacterBody2D
func _ready():
	paddle_center = paddle_height / 2
	collision_shape.shape.extents = Vector2(paddle_width/2, paddle_center)

func _physics_process(_delta):
	MoveComputer()
	move_and_slide()
	position.y = clamp(position.y, paddle_center, screen_size.y - paddle_center)
	
func MoveComputer() -> void:
	var direction = ((screen_size/2) - position).normalized()\
	if position.distance_to(ball.position) > 700.0\
	else (ball.position - position).normalized()
	velocity.y = direction.y * speed * 4.5
