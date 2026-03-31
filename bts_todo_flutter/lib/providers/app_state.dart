import 'package:flutter/material.dart';
import 'package:uuid/uuid.dart';
import '../models/task.dart';
import '../services/data_service.dart';

class AppState with ChangeNotifier {
  final DataService _dataService = DataService();
  final Uuid _uuid = const Uuid();

  List<Task> _tasks = [];
  String _currentTheme = 'purple';
  String _currentBias = 'V';
  String? _customBgPath;
  double _panelOpacity = 0.8;

  List<Task> get tasks => _tasks;
  String get currentTheme => _currentTheme;
  String get currentBias => _currentBias;
  String? get customBgPath => _customBgPath;
  double get panelOpacity => _panelOpacity;

  AppState() {
    _loadData();
  }

  Future<void> _loadData() async {
    _tasks = await _dataService.loadTasks();
    _currentTheme = await _dataService.loadTheme();
    _currentBias = await _dataService.loadBias();
    _customBgPath = await _dataService.loadCustomBg();
    _panelOpacity = await _dataService.loadOpacity();
    notifyListeners();
  }

  void addTask(String text) {
    final newTask = Task(id: _uuid.v4(), text: text);
    _tasks.add(newTask);
    _dataService.saveTasks(_tasks);
    notifyListeners();
  }

  void toggleTask(String id) {
    final index = _tasks.indexWhere((t) => t.id == id);
    if (index != -1) {
      _tasks[index].completed = !_tasks[index].completed;
      _dataService.saveTasks(_tasks);
      notifyListeners();
    }
  }

  void deleteTask(String id) {
    _tasks.removeWhere((t) => t.id == id);
    _dataService.saveTasks(_tasks);
    notifyListeners();
  }

  void setTheme(String theme) {
    _currentTheme = theme;
    _dataService.saveTheme(theme);
    notifyListeners();
  }

  void setBias(String bias) {
    _currentBias = bias;
    _dataService.saveBias(bias);
    notifyListeners();
  }

  void setCustomBg(String? path) {
    _customBgPath = path;
    if (path != null) {
      _dataService.saveCustomBg(path);
    }
    notifyListeners();
  }

  void setOpacity(double opacity) {
    _panelOpacity = opacity;
    _dataService.saveOpacity(opacity);
    notifyListeners();
  }

  bool get allTasksCompleted => _tasks.isNotEmpty && _tasks.every((t) => t.completed);
}
