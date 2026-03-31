import 'package:flutter/material.dart';

class BTSTheme {
  final String name;
  final Color primary;
  final Color secondary;
  final Color bg;
  final Color text;
  final String? bgImage;

  BTSTheme({
    required this.name,
    required this.primary,
    required this.secondary,
    required this.bg,
    required this.text,
    this.bgImage,
  });
}

class AppTheme {
  static final Map<String, BTSTheme> themes = {
    'purple': BTSTheme(
      name: 'Purple Love',
      primary: const Color(0xFFD9B3FF),
      secondary: const Color(0xFFA259FF),
      bg: const Color(0xFF1A0B2E),
      text: const Color(0xFFFFFFFF),
      // bgImage: 'assets/foto.jfif', // We will handle assets later
    ),
    'butter': BTSTheme(
      name: 'Butter',
      primary: const Color(0xFFFFA500),
      secondary: const Color(0xFFFFFF00),
      bg: const Color(0xFFFFFACD),
      text: const Color(0xFF333333),
    ),
    'dynamite': BTSTheme(
      name: 'Dynamite',
      primary: const Color(0xFFFF69B4),
      secondary: const Color(0xFF87CEEB),
      bg: const Color(0xFFE0FFFF),
      text: const Color(0xFF333333),
    ),
    'dark': BTSTheme(
      name: 'Dark Mode',
      primary: const Color(0xFFBB86FC),
      secondary: const Color(0xFF03DAC6),
      bg: const Color(0xFF121212),
      text: const Color(0xFFFFFFFF),
    ),
  };

  static BTSTheme getTheme(String name) {
    return themes[name.toLowerCase()] ?? themes['purple']!;
  }
}
