import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';

class BotSettingsScreen extends StatefulWidget {
  const BotSettingsScreen({super.key});

  @override
  State<BotSettingsScreen> createState() => _BotSettingsScreenState();
}

class _BotSettingsScreenState extends State<BotSettingsScreen> {
  TimeOfDay _morningTime = const TimeOfDay(hour: 7, minute: 0);
  TimeOfDay _eveningTime = const TimeOfDay(hour: 23, minute: 30);
  bool _isLoading = false;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFFFFF5EE),
      appBar: AppBar(
        title: const Text('Настройка Ватсона'),
        backgroundColor: const Color(0xFFE67E6B),
        foregroundColor: Colors.white,
        elevation: 0,
      ),
      body: _isLoading
          ? const Center(child: CircularProgressIndicator())
          : SingleChildScrollView(
              padding: const EdgeInsets.all(24.0),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  // Заголовок
                  const Text(
                    'Когда получать маркетинговые уведомления?',
                    style: TextStyle(
                      fontSize: 24,
                      fontWeight: FontWeight.bold,
                      color: Color(0xFF8B4513),
                    ),
                  ),
                  
                  const SizedBox(height: 8),
                  
                  const Text(
                    'Выберите удобное время для утренних и вечерних маркетинговых уведомлений',
                    style: TextStyle(
                      fontSize: 16,
                      color: Color(0xFF8B4513),
                    ),
                  ),
                  
                  const SizedBox(height: 40),
                  
                  // Утреннее время
                  _buildTimeCard(
                    icon: Icons.wb_sunny,
                    title: 'Утренние маркетинговые уведомления',
                    subtitle: 'Время для важных маркетинговых уведомлений',
                    time: _morningTime,
                    onTap: () => _selectTime(context, true),
                    color: Colors.orange,
                  ),
                  
                  const SizedBox(height: 20),
                  
                  // Вечернее время
                  _buildTimeCard(
                    icon: Icons.nightlight_round,
                    title: 'Вечерние маркетинговые уведомления',
                    subtitle: 'Время для итогов маркетинговых кампаний',
                    time: _eveningTime,
                    onTap: () => _selectTime(context, false),
                    color: Colors.indigo,
                  ),
                  
                  const SizedBox(height: 40),
                  
                  // Информация о приватности
                  Container(
                    padding: const EdgeInsets.all(16),
                    decoration: BoxDecoration(
                      color: Colors.green[50],
                      borderRadius: BorderRadius.circular(12),
                      border: Border.all(color: Colors.green[200]!),
                    ),
                    child: Row(
                      children: [
                        Icon(
                          Icons.security,
                          color: Colors.green[600],
                          size: 24,
                        ),
                        const SizedBox(width: 12),
                        const Expanded(
                          child: Text(
                            'После настройки все сообщения будут удалены для обеспечения вашей приватности',
                            style: TextStyle(
                              color: Colors.green,
                              fontSize: 14,
                            ),
                          ),
                        ),
                      ],
                    ),
                  ),
                  
                  const SizedBox(height: 40),
                  
                  // Кнопка сохранения
                  SizedBox(
                    width: double.infinity,
                    height: 56,
                    child: ElevatedButton(
                      onPressed: _saveSettings,
                      style: ElevatedButton.styleFrom(
                        backgroundColor: const Color(0xFFE67E6B),
                        foregroundColor: Colors.white,
                        shape: RoundedRectangleBorder(
                          borderRadius: BorderRadius.circular(16),
                        ),
                        elevation: 8,
                      ),
                      child: const Text(
                        'Сохранить настройки',
                        style: TextStyle(
                          fontSize: 18,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                    ),
                  ),
                ],
              ),
            ),
    );
  }

  Widget _buildTimeCard({
    required IconData icon,
    required String title,
    required String subtitle,
    required TimeOfDay time,
    required VoidCallback onTap,
    required Color color,
  }) {
    return GestureDetector(
      onTap: onTap,
      child: Container(
        padding: const EdgeInsets.all(20),
        decoration: BoxDecoration(
          color: Colors.white,
          borderRadius: BorderRadius.circular(16),
          boxShadow: [
            BoxShadow(
              color: Colors.grey.withOpacity(0.1),
              blurRadius: 10,
              offset: const Offset(0, 5),
            ),
          ],
        ),
        child: Row(
          children: [
            Container(
              width: 60,
              height: 60,
              decoration: BoxDecoration(
                color: color.withOpacity(0.1),
                borderRadius: BorderRadius.circular(12),
              ),
              child: Icon(
                icon,
                color: color,
                size: 30,
              ),
            ),
            const SizedBox(width: 16),
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    title,
                    style: const TextStyle(
                      fontSize: 18,
                      fontWeight: FontWeight.bold,
                      color: Color(0xFF8B4513),
                    ),
                  ),
                  const SizedBox(height: 4),
                  Text(
                    subtitle,
                    style: const TextStyle(
                      fontSize: 14,
                      color: Color(0xFF8B4513),
                    ),
                  ),
                ],
              ),
            ),
            Column(
              children: [
                Text(
                  '${time.hour.toString().padLeft(2, '0')}:${time.minute.toString().padLeft(2, '0')}',
                  style: TextStyle(
                    fontSize: 24,
                    fontWeight: FontWeight.bold,
                    color: color,
                  ),
                ),
                const Text(
                  'Нажмите для изменения',
                  style: TextStyle(
                    fontSize: 12,
                    color: Colors.grey,
                  ),
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }

  Future<void> _selectTime(BuildContext context, bool isMorning) async {
    final TimeOfDay? picked = await showTimePicker(
      context: context,
      initialTime: isMorning ? _morningTime : _eveningTime,
      builder: (context, child) {
        return Theme(
          data: Theme.of(context).copyWith(
            colorScheme: const ColorScheme.light(
              primary: Color(0xFFE67E6B),
              onPrimary: Colors.white,
              surface: Colors.white,
              onSurface: Colors.black,
            ),
          ),
          child: child!,
        );
      },
    );

    if (picked != null) {
      setState(() {
        if (isMorning) {
          _morningTime = picked;
        } else {
          _eveningTime = picked;
        }
      });
    }
  }

  Future<void> _saveSettings() async {
    setState(() {
      _isLoading = true;
    });

    try {
      final prefs = await SharedPreferences.getInstance();
      
      // Сохраняем настройки времени
      await prefs.setInt('bot_morning_hour', _morningTime.hour);
      await prefs.setInt('bot_morning_minute', _morningTime.minute);
      await prefs.setInt('bot_evening_hour', _eveningTime.hour);
      await prefs.setInt('bot_evening_minute', _eveningTime.minute);
      
      // Отмечаем, что настройка бота завершена
      await prefs.setBool('bot_setup_complete', true);
      
      // Показываем сообщение об успехе
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(
            content: Text('Настройки Ватсона сохранены! Все сообщения удалены.'),
            backgroundColor: Colors.green,
            duration: Duration(seconds: 2),
          ),
        );
      }
      
      // Переходим на экран ожидания
      if (mounted) {
        Navigator.pushReplacementNamed(context, '/bot_waiting');
      }
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(
            content: Text('Ошибка при сохранении настроек'),
            backgroundColor: Colors.red,
          ),
        );
      }
    } finally {
      setState(() {
        _isLoading = false;
      });
    }
  }
}