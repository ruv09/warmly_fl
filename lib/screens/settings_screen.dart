import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';

class SettingsScreen extends StatefulWidget {
  const SettingsScreen({super.key});

  @override
  State<SettingsScreen> createState() => _SettingsScreenState();
}

class _SettingsScreenState extends State<SettingsScreen> {
  String language = 'ru';
  bool pushMorning = true;
  bool pushEvening = true;

  @override
  void initState() {
    super.initState();
    _load();
  }

  Future<void> _load() async {
    final p = await SharedPreferences.getInstance();
    setState(() {
      language = p.getString('lang') ?? 'ru';
      pushMorning = p.getBool('push_morning') ?? true;
      pushEvening = p.getBool('push_evening') ?? true;
    });
  }

  Future<void> _save() async {
    final p = await SharedPreferences.getInstance();
    await p.setString('lang', language);
    await p.setBool('push_morning', pushMorning);
    await p.setBool('push_evening', pushEvening);
    if (mounted) {
      ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text('Сохранено')));
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Настройки'), backgroundColor: const Color(0xFF6A4C93)),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          const Text('Уведомления от Вселенной', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
          const SizedBox(height: 8),
          SwitchListTile(
            value: pushMorning, 
            onChanged: (v) => setState(() => pushMorning = v), 
            title: const Text('Утренние послания'),
            subtitle: const Text('Каждый день в 8:00'),
          ),
          SwitchListTile(
            value: pushEvening, 
            onChanged: (v) => setState(() => pushEvening = v), 
            title: const Text('Вечерние послания'),
            subtitle: const Text('Каждый день в 22:00'),
          ),

          const Divider(),
          ListTile(
            title: const Text('Язык'),
            subtitle: Text(language == 'ru' ? 'Русский' : 'English'),
            onTap: () => setState(() => language = language == 'ru' ? 'en' : 'ru'),
          ),

          const SizedBox(height: 12),
          ElevatedButton(onPressed: _save, child: const Text('Сохранить изменения')),
        ],
      ),
    );
  }
}