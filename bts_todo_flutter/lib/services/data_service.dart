import 'dart:convert';
import 'package:shared_preferences/shared_preferences.dart';
import '../models/task.dart';

class DataService {
  static const String _tasksKey = 'tasks';
  static const String _themeKey = 'theme';
  static const String _biasKey = 'bias';
  static const String _bgKey = 'custom_bg';
  static const String _opacityKey = 'panel_opacity';

  Future<void> saveTasks(List<Task> tasks) async {
    final prefs = await SharedPreferences.getInstance();
    final String encodedData = json.encode(
      tasks.map((task) => task.toJson()).toList(),
    );
    await prefs.setString(_tasksKey, encodedData);
  }

  Future<List<Task>> loadTasks() async {
    final prefs = await SharedPreferences.getInstance();
    final String? tasksString = prefs.getString(_tasksKey);
    if (tasksString == null) return [];

    final List<dynamic> jsonList = json.decode(tasksString);
    return jsonList.map((json) => Task.fromJson(json)).toList();
  }

  Future<void> saveTheme(String theme) async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString(_themeKey, theme);
  }

  Future<String> loadTheme() async {
    final prefs = await SharedPreferences.getInstance();
    return prefs.getString(_themeKey) ?? 'purple';
  }

  Future<void> saveBias(String bias) async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString(_biasKey, bias);
  }

  Future<String> loadBias() async {
    final prefs = await SharedPreferences.getInstance();
    return prefs.getString(_biasKey) ?? 'V';
  }

  Future<void> saveCustomBg(String path) async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString(_bgKey, path);
  }

  Future<String?> loadCustomBg() async {
    final prefs = await SharedPreferences.getInstance();
    return prefs.getString(_bgKey);
  }

  Future<void> saveOpacity(double opacity) async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setDouble(_opacityKey, opacity);
  }

  Future<double> loadOpacity() async {
    final prefs = await SharedPreferences.getInstance();
    return prefs.getDouble(_opacityKey) ?? 0.8;
  }
}
