extends Actor

@onready var collision_shape: = get_node("CollisionShape2D")

func _ready():
	paddle_center = paddle_height / 2
	collision_shape.shape.extents = Vector2(paddle_width/2, paddle_center)
	
func _physics_process(_delta):
	get_input()
	position.y = clamp(position.y, paddle_center, screen_size.y - paddle_center)
	move_and_slide()
	
func get_input() -> void:
	var direction = Input.get_axis("move_up", "move_down")
	velocity.y = direction * speed * 2
	
