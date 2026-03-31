import 'package:flutter/material.dart';
import '../models/task.dart';
import '../theme/app_theme.dart';

class TaskItem extends StatelessWidget {
  final Task task;
  final BTSTheme theme;
  final VoidCallback onToggle;
  final VoidCallback onDelete;

  const TaskItem({
    super.key,
    required this.task,
    required this.theme,
    required this.onToggle,
    required this.onDelete,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      margin: const EdgeInsets.symmetric(vertical: 5),
      padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 5),
      decoration: BoxDecoration(
        color: theme.text.withOpacity(0.1),
        borderRadius: BorderRadius.circular(10),
      ),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          Row(
            children: [
              Checkbox(
                value: task.completed,
                onChanged: (_) => onToggle(),
                activeColor: theme.primary,
                checkColor: theme.bg,
                side: BorderSide(color: theme.text.withOpacity(0.5)),
              ),
              Text(
                task.text,
                style: TextStyle(
                  color: theme.text,
                  fontSize: 16,
                  decoration: task.completed
                      ? TextDecoration.lineThrough
                      : TextDecoration.none,
                  decorationColor: theme.text,
                ),
              ),
            ],
          ),
          IconButton(
            icon: const Icon(Icons.delete_outline_rounded),
            color: Colors.red[400],
            onPressed: onDelete,
            tooltip: 'Delete Task',
          ),
        ],
      ),
    );
  }
}
