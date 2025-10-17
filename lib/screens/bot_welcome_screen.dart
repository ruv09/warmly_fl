import 'package:flutter/material.dart';

class BotWelcomeScreen extends StatelessWidget {
  const BotWelcomeScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFFFFF5EE),
      body: SafeArea(
        child: Padding(
          padding: const EdgeInsets.all(32.0),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              // Иконка бота
              Container(
                width: 120,
                height: 120,
                decoration: BoxDecoration(
                  color: const Color(0xFFE67E6B),
                  shape: BoxShape.circle,
                  boxShadow: [
                    BoxShadow(
                      color: const Color(0xFFE67E6B).withOpacity(0.3),
                      blurRadius: 20,
                      offset: const Offset(0, 10),
                    ),
                  ],
                ),
                child: const Icon(
                  Icons.smart_toy,
                  size: 60,
                  color: Colors.white,
                ),
              ),
              
              const SizedBox(height: 40),
              
              // Заголовок
              const Text(
                'Привет!',
                style: TextStyle(
                  fontSize: 32,
                  fontWeight: FontWeight.bold,
                  color: Color(0xFF8B4513),
                ),
                textAlign: TextAlign.center,
              ),
              
              const SizedBox(height: 20),
              
              // Описание бота
              Container(
                padding: const EdgeInsets.all(24),
                decoration: BoxDecoration(
                  color: Colors.white,
                  borderRadius: BorderRadius.circular(20),
                  boxShadow: [
                    BoxShadow(
                      color: Colors.grey.withOpacity(0.1),
                      blurRadius: 15,
                      offset: const Offset(0, 8),
                    ),
                  ],
                ),
                child: Column(
                  children: [
                    const Text(
                      'Я Ватсон 🤖',
                      style: TextStyle(
                        fontSize: 24,
                        fontWeight: FontWeight.bold,
                        color: Color(0xFFE67E6B),
                      ),
                    ),
                    const SizedBox(height: 16),
                    const Text(
                      'Первый в мире маркетинга WhatsApp-лендинг бот! '
                      'Я стану вашим лучшим сотрудником и незаменимым помощником! '
                      'Просто настройте расписание, и я буду присылать вам важные '
                      'маркетинговые уведомления утром и вечером.',
                      style: TextStyle(
                        fontSize: 16,
                        color: Color(0xFF8B4513),
                        height: 1.5,
                      ),
                      textAlign: TextAlign.center,
                    ),
                    const SizedBox(height: 20),
                    Row(
                      mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                      children: [
                        _buildFeature(
                          Icons.schedule,
                          'Маркетинговое расписание',
                          'Уведомления в удобное время',
                        ),
                        _buildFeature(
                          Icons.trending_up,
                          'WhatsApp-лендинги',
                          'Эффективные кампании',
                        ),
                        _buildFeature(
                          Icons.security,
                          'Конфиденциальность',
                          'Все данные защищены',
                        ),
                      ],
                    ),
                  ],
                ),
              ),
              
              const SizedBox(height: 40),
              
              // Кнопка "Начать"
              SizedBox(
                width: double.infinity,
                height: 56,
                child: ElevatedButton(
                  onPressed: () {
                    Navigator.pushNamed(context, '/bot_settings');
                  },
                  style: ElevatedButton.styleFrom(
                    backgroundColor: const Color(0xFFE67E6B),
                    foregroundColor: Colors.white,
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(16),
                    ),
                    elevation: 8,
                  ),
                  child: const Text(
                    'Начать настройку',
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
      ),
    );
  }

  Widget _buildFeature(IconData icon, String title, String description) {
    return Expanded(
      child: Column(
        children: [
          Icon(
            icon,
            size: 32,
            color: const Color(0xFFE67E6B),
          ),
          const SizedBox(height: 8),
          Text(
            title,
            style: const TextStyle(
              fontSize: 14,
              fontWeight: FontWeight.bold,
              color: Color(0xFF8B4513),
            ),
            textAlign: TextAlign.center,
          ),
          const SizedBox(height: 4),
          Text(
            description,
            style: const TextStyle(
              fontSize: 12,
              color: Color(0xFF8B4513),
            ),
            textAlign: TextAlign.center,
          ),
        ],
      ),
    );
  }
}