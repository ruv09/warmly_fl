import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:flutter_local_notifications/flutter_local_notifications.dart';
import 'dart:async';

class WaitingScreen extends StatefulWidget {
  @override
  _WaitingScreenState createState() => _WaitingScreenState();
}

class _WaitingScreenState extends State<WaitingScreen> {
  final FlutterLocalNotificationsPlugin _notifications = FlutterLocalNotificationsPlugin();
  TimeOfDay? _morningTime;
  TimeOfDay? _eveningTime;
  Timer? _timer;
  String _nextMessageTime = '';

  @override
  void initState() {
    super.initState();
    _initializeNotifications();
    _loadSettings();
    _startTimer();
  }

  @override
  void dispose() {
    _timer?.cancel();
    super.dispose();
  }

  Future<void> _initializeNotifications() async {
    const AndroidInitializationSettings initializationSettingsAndroid =
        AndroidInitializationSettings('@mipmap/ic_launcher');
    
    const InitializationSettings initializationSettings =
        InitializationSettings(android: initializationSettingsAndroid);
    
    await _notifications.initialize(initializationSettings);
  }

  Future<void> _loadSettings() async {
    final prefs = await SharedPreferences.getInstance();
    
    final morningHour = prefs.getInt('morning_hour') ?? 7;
    final morningMinute = prefs.getInt('morning_minute') ?? 0;
    final eveningHour = prefs.getInt('evening_hour') ?? 23;
    final eveningMinute = prefs.getInt('evening_minute') ?? 30;
    
    setState(() {
      _morningTime = TimeOfDay(hour: morningHour, minute: morningMinute);
      _eveningTime = TimeOfDay(hour: eveningHour, minute: eveningMinute);
    });
    
    _updateNextMessageTime();
  }

  void _startTimer() {
    _timer = Timer.periodic(Duration(minutes: 1), (timer) {
      _checkForScheduledMessages();
      _updateNextMessageTime();
    });
  }

  void _updateNextMessageTime() {
    if (_morningTime == null || _eveningTime == null) return;
    
    final now = DateTime.now();
    final currentTime = TimeOfDay.fromDateTime(now);
    
    // Определяем следующее время сообщения
    TimeOfDay nextTime;
    if (currentTime.hour < _morningTime!.hour || 
        (currentTime.hour == _morningTime!.hour && currentTime.minute < _morningTime!.minute)) {
      nextTime = _morningTime!;
    } else if (currentTime.hour < _eveningTime!.hour || 
               (currentTime.hour == _eveningTime!.hour && currentTime.minute < _eveningTime!.minute)) {
      nextTime = _eveningTime!;
    } else {
      // Следующее сообщение будет завтра утром
      nextTime = _morningTime!;
    }
    
    setState(() {
      _nextMessageTime = '${nextTime.hour.toString().padLeft(2, '0')}:${nextTime.minute.toString().padLeft(2, '0')}';
    });
  }

  Future<void> _checkForScheduledMessages() async {
    final now = DateTime.now();
    final currentTime = TimeOfDay.fromDateTime(now);
    
    if (_morningTime != null && 
        currentTime.hour == _morningTime!.hour && 
        currentTime.minute == _morningTime!.minute) {
      await _sendMorningMessage();
    }
    
    if (_eveningTime != null && 
        currentTime.hour == _eveningTime!.hour && 
        currentTime.minute == _eveningTime!.minute) {
      await _sendEveningMessage();
    }
  }

  Future<void> _sendMorningMessage() async {
    await _notifications.show(
      1,
      'Доброе утро! Ватсон здесь 🤖',
      'Время для утренних маркетинговых уведомлений. Проверьте WhatsApp-лендинги!',
      const NotificationDetails(
        android: AndroidNotificationDetails(
          'morning_messages',
          'Утренние маркетинговые уведомления',
          importance: Importance.high,
          priority: Priority.high,
        ),
      ),
    );
  }

  Future<void> _sendEveningMessage() async {
    await _notifications.show(
      2,
      'Добрый вечер! Ватсон здесь 🤖',
      'Время для вечерних маркетинговых итогов. Проверьте результаты кампаний!',
      const NotificationDetails(
        android: AndroidNotificationDetails(
          'evening_messages',
          'Вечерние маркетинговые уведомления',
          importance: Importance.high,
          priority: Priority.high,
        ),
      ),
    );
  }

  Future<void> _resetSettings() async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.clear();
    
    Navigator.pushReplacementNamed(context, '/');
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.blue[50],
      appBar: AppBar(
        title: Text('Ватсон 🤖'),
        backgroundColor: Colors.blue,
        foregroundColor: Colors.white,
        elevation: 0,
        actions: [
          IconButton(
            icon: Icon(Icons.settings),
            onPressed: _resetSettings,
            tooltip: 'Сбросить настройки',
          ),
        ],
      ),
      body: Padding(
        padding: const EdgeInsets.all(24.0),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            // Статус бота
            Container(
              width: 120,
              height: 120,
              decoration: BoxDecoration(
                color: Colors.green,
                shape: BoxShape.circle,
                boxShadow: [
                  BoxShadow(
                    color: Colors.green.withOpacity(0.3),
                    blurRadius: 20,
                    offset: Offset(0, 10),
                  ),
                ],
              ),
              child: Icon(
                Icons.check_circle,
                size: 60,
                color: Colors.white,
              ),
            ),
            
            SizedBox(height: 40),
            
            Text(
              'Бот активен!',
              style: TextStyle(
                fontSize: 32,
                fontWeight: FontWeight.bold,
                color: Colors.green[700],
              ),
            ),
            
            SizedBox(height: 20),
            
            Text(
              'Я буду присылать вам маркетинговые уведомления по расписанию',
              style: TextStyle(
                fontSize: 18,
                color: Colors.grey[600],
              ),
              textAlign: TextAlign.center,
            ),
            
            SizedBox(height: 40),
            
            // Настройки времени
            Container(
              padding: EdgeInsets.all(20),
              decoration: BoxDecoration(
                color: Colors.white,
                borderRadius: BorderRadius.circular(16),
                boxShadow: [
                  BoxShadow(
                    color: Colors.grey.withOpacity(0.1),
                    blurRadius: 10,
                    offset: Offset(0, 5),
                  ),
                ],
              ),
              child: Column(
                children: [
                  if (_morningTime != null)
                    _buildTimeInfo(
                      icon: Icons.wb_sunny,
                      title: 'Утренние маркетинговые уведомления',
                      time: '${_morningTime!.hour.toString().padLeft(2, '0')}:${_morningTime!.minute.toString().padLeft(2, '0')}',
                      color: Colors.orange,
                    ),
                  
                  if (_morningTime != null && _eveningTime != null)
                    Divider(height: 20),
                  
                  if (_eveningTime != null)
                    _buildTimeInfo(
                      icon: Icons.nightlight_round,
                      title: 'Вечерние маркетинговые уведомления',
                      time: '${_eveningTime!.hour.toString().padLeft(2, '0')}:${_eveningTime!.minute.toString().padLeft(2, '0')}',
                      color: Colors.indigo,
                    ),
                ],
              ),
            ),
            
            SizedBox(height: 30),
            
            // Следующее сообщение
            if (_nextMessageTime.isNotEmpty)
              Container(
                padding: EdgeInsets.all(16),
                decoration: BoxDecoration(
                  color: Colors.blue[50],
                  borderRadius: BorderRadius.circular(12),
                  border: Border.all(color: Colors.blue[200]!),
                ),
                child: Row(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    Icon(
                      Icons.schedule,
                      color: Colors.blue[600],
                      size: 20,
                    ),
                    SizedBox(width: 8),
                    Text(
                      'Следующее сообщение в $_nextMessageTime',
                      style: TextStyle(
                        color: Colors.blue[700],
                        fontSize: 16,
                        fontWeight: FontWeight.w500,
                      ),
                    ),
                  ],
                ),
              ),
            
            SizedBox(height: 40),
            
            // Информация о приватности
            Container(
              padding: EdgeInsets.all(16),
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
                  SizedBox(width: 12),
                  Expanded(
                    child: Text(
                      'Все сообщения удалены. Ваша приватность защищена.',
                      style: TextStyle(
                        color: Colors.green[700],
                        fontSize: 14,
                      ),
                    ),
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildTimeInfo({
    required IconData icon,
    required String title,
    required String time,
    required Color color,
  }) {
    return Row(
      children: [
        Icon(
          icon,
          color: color,
          size: 24,
        ),
        SizedBox(width: 12),
        Expanded(
          child: Text(
            title,
            style: TextStyle(
              fontSize: 16,
              fontWeight: FontWeight.w500,
              color: Colors.grey[700],
            ),
          ),
        ),
        Text(
          time,
          style: TextStyle(
            fontSize: 18,
            fontWeight: FontWeight.bold,
            color: color,
          ),
        ),
      ],
    );
  }
}