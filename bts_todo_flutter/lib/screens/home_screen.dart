import 'dart:io';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:file_picker/file_picker.dart';
import 'package:audioplayers/audioplayers.dart';
import '../providers/app_state.dart';
import '../theme/app_theme.dart';
import '../widgets/glass_container.dart';
import '../widgets/task_item.dart';

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  final TextEditingController _taskController = TextEditingController();
  final AudioPlayer _audioPlayer = AudioPlayer();
  bool _showCelebration = false;

  @override
  void dispose() {
    _taskController.dispose();
    _audioPlayer.dispose();
    super.dispose();
  }

  Future<void> _pickFile(BuildContext context) async {
    FilePickerResult? result = await FilePicker.platform.pickFiles(
      type: FileType.image,
    );

    if (result != null && result.files.single.path != null) {
      if (mounted) {
        Provider.of<AppState>(context, listen: false).setCustomBg(result.files.single.path);
      }
    }
  }

  Future<void> _playCelebration() async {
    setState(() {
      _showCelebration = true;
    });

    // Play sound (assuming success.mp3 is in assets)
    // Note: You need to add assets to pubspec.yaml
    try {
        await _audioPlayer.play(AssetSource('success.mp3'));
    } catch (e) {
        print("Audio error: $e");
    }

    await Future.delayed(const Duration(seconds: 4));

    if (mounted) {
      setState(() {
        _showCelebration = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    final appState = Provider.of<AppState>(context);
    final theme = AppTheme.getTheme(appState.currentTheme);

    // Calculate progress
    int completed = appState.tasks.where((t) => t.completed).length;
    double progress = appState.tasks.isEmpty ? 0 : completed / appState.tasks.length;

    return Scaffold(
      backgroundColor: theme.bg, // Fallback background
      floatingActionButton: FloatingActionButton(
        backgroundColor: theme.primary,
        onPressed: () {
          showModalBottomSheet(
            context: context,
            backgroundColor: theme.bg,
            builder: (context) => Container(
              padding: EdgeInsets.only(
                bottom: MediaQuery.of(context).viewInsets.bottom + 20,
                left: 20,
                right: 20,
                top: 20,
              ),
              child: Column(
                mainAxisSize: MainAxisSize.min,
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text("Nova Tarefa", style: TextStyle(color: theme.text, fontSize: 18, fontWeight: FontWeight.bold)),
                  const SizedBox(height: 10),
                  Row(
                    children: [
                      Expanded(
                        child: TextField(
                          controller: _taskController,
                          style: TextStyle(color: theme.text),
                          decoration: InputDecoration(
                            hintText: "Digite sua tarefa...",
                            hintStyle: TextStyle(color: theme.text.withOpacity(0.5)),
                            border: InputBorder.none,
                          ),
                        ),
                      ),
                      IconButton(
                        icon: Icon(Icons.send, color: theme.primary),
                        onPressed: () {
                          if (_taskController.text.isNotEmpty) {
                            appState.addTask(_taskController.text);
                            _taskController.clear();
                            Navigator.pop(context);
                          }
                        },
                      )
                    ],
                  )
                ],
              ),
            ),
          );
        },
        child: Icon(Icons.add, color: theme.bg),
      ),
      body: Stack(
        children: [
          // Background Image
          if (appState.customBgPath != null)
            Positioned.fill(
              child: Image.file(
                File(appState.customBgPath!),
                fit: BoxFit.cover,
              ),
            )
          else if (theme.bgImage != null && theme.bgImage!.isNotEmpty)
             // Placeholder for asset image logic
             // Positioned.fill(child: Image.asset(theme.bgImage!, fit: BoxFit.cover))
             Container(color: theme.bg)
          else
            Container(color: theme.bg),

          // Main Content
          Center(
            child: SingleChildScrollView(
              child: ConstrainedBox(
                constraints: const BoxConstraints(maxWidth: 600),
                child: Padding(
                  padding: const EdgeInsets.all(20.0),
                  child: GlassContainer(
                    color: theme.bg,
                    opacity: appState.panelOpacity,
                    child: Padding(
                      padding: const EdgeInsets.all(20.0),
                      child: Column(
                        mainAxisSize: MainAxisSize.min,
                        children: [
                          // Header
                          Row(
                            mainAxisAlignment: MainAxisAlignment.spaceBetween,
                            children: [
                              Text(
                                "Olá, ${appState.currentBias} Stan! 💜",
                                style: TextStyle(
                                  color: theme.text,
                                  fontSize: 24,
                                  fontWeight: FontWeight.bold,
                                ),
                              ),
                              IconButton(
                                icon: Icon(Icons.settings, color: theme.text),
                                onPressed: () => _showSettings(context, appState, theme),
                              ),
                            ],
                          ),
                          const SizedBox(height: 10),

                          // Progress Bar
                          LinearProgressIndicator(
                            value: progress,
                            backgroundColor: theme.text.withOpacity(0.1),
                            color: theme.primary,
                            minHeight: 8,
                            borderRadius: BorderRadius.circular(4),
                          ),
                          const SizedBox(height: 20),

                          // Task List
                          if (appState.tasks.isEmpty)
                            Padding(
                              padding: const EdgeInsets.all(20.0),
                              child: Text(
                                "Nenhuma tarefa ainda...",
                                style: TextStyle(color: theme.text.withOpacity(0.5)),
                              ),
                            )
                          else
                            ...appState.tasks.map((task) => TaskItem(
                              task: task,
                              theme: theme,
                              onToggle: () {
                                appState.toggleTask(task.id);
                                if (appState.allTasksCompleted) {
                                    _playCelebration();
                                }
                              },
                              onDelete: () => appState.deleteTask(task.id),
                            )),
                        ],
                      ),
                    ),
                  ),
                ),
              ),
            ),
          ),

          // Celebration Overlay
          if (_showCelebration)
            Positioned.fill(
              child: Image.network(
                "https://media.giphy.com/media/l0HlHFRbmaZtBRhXG/giphy.gif",
                fit: BoxFit.contain,
              ),
            ),
        ],
      ),
    );
  }

  void _showSettings(BuildContext context, AppState appState, BTSTheme theme) {
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text("Configurações"),
        content: Column(
          mainAxisSize: MainAxisSize.min,
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text("Tema", style: TextStyle(fontWeight: FontWeight.bold)),
            DropdownButton<String>(
              value: appState.currentTheme,
              isExpanded: true,
              items: AppTheme.themes.keys.map((String key) {
                return DropdownMenuItem<String>(
                  value: key,
                  child: Text(AppTheme.getTheme(key).name),
                );
              }).toList(),
              onChanged: (String? newValue) {
                if (newValue != null) appState.setTheme(newValue);
              },
            ),
            const SizedBox(height: 15),
            const Text("Bias", style: TextStyle(fontWeight: FontWeight.bold)),
            DropdownButton<String>(
              value: appState.currentBias,
              isExpanded: true,
              items: ["RM", "Jin", "Suga", "J-Hope", "Jimin", "V", "Jungkook"]
                  .map((String value) {
                return DropdownMenuItem<String>(
                  value: value,
                  child: Text(value),
                );
              }).toList(),
              onChanged: (String? newValue) {
                if (newValue != null) appState.setBias(newValue);
              },
            ),
            const SizedBox(height: 15),
            const Text("Transparência", style: TextStyle(fontWeight: FontWeight.bold)),
            Slider(
              value: appState.panelOpacity,
              min: 0.1,
              max: 1.0,
              onChanged: (val) => appState.setOpacity(val),
            ),
            const SizedBox(height: 10),
            ElevatedButton(
              onPressed: () => _pickFile(context),
              child: const Text("Escolher Fundo"),
            ),
          ],
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context),
            child: const Text("Fechar"),
          ),
        ],
      ),
    );
  }
}
