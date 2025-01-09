extends CharacterBody2D

signal gameover

@export var speed = 300.0
@export var ball_radius: = 10.0

@onready var collision_shape: CollisionShape2D = get_node("CollisionShape2D")

const add_speed = 1.04

var user_direction = true
var random = RandomNumberGenerator.new()

func _ready():
	random.randomize()
	
	
func _draw():
	draw_circle(Vector2.ZERO, ball_radius, Color.WHITE)
	collision_shape.shape.radius = ball_radius
	
func _on_screen_exited() -> void:
	user_direction = global_position.x > 0
	gameover.emit(user_direction)
	
func _physics_process(delta):
	var collision = move_and_collide(velocity * delta)
	if collision:
		velocity = velocity.bounce(collision.get_normal()) * add_speed


func start_position(pos: Vector2):
	position = pos


func direction() -> void:
	velocity = Vector2(
		-speed if user_direction else speed,
		speed if random.randi_range(-1, 2) > 0 else -speed
			
	)
