class Task {
  String id;
  String text;
  bool completed;

  Task({required this.id, required this.text, this.completed = false});

  // Convert Task to Map for saving
  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'text': text,
      'completed': completed,
    };
  }

  // Create Task from Map
  factory Task.fromJson(Map<String, dynamic> json) {
    return Task(
      id: json['id'],
      text: json['text'],
      completed: json['completed'],
    );
  }
}
