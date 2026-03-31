import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'providers/app_state.dart';
import 'screens/home_screen.dart';

void main() {
  runApp(
    MultiProvider(
      providers: [
        ChangeNotifierProvider(create: (_) => AppState()),
      ],
      child: const BTSToDoApp(),
    ),
  );
}

class BTSToDoApp extends StatelessWidget {
  const BTSToDoApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'BTS To-Do List',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        useMaterial3: true,
        fontFamily: 'Roboto', // Ensure fonts are loaded if using google_fonts
      ),
      home: const HomeScreen(),
    );
  }
}
