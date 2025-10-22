import 'dart:math';
import 'package:flutter/material.dart';
import '../widgets/cosmic_animations.dart';
import '../services/sound_service.dart';
import 'stats_screen.dart';

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  String phrase = '';

  @override
  void initState() {
    super.initState();
    _loadPhrase();
    // Воспроизводим космический звук при загрузке
    SoundService().playCosmicSound();
  }

  void _loadPhrase() {
    final now = TimeOfDay.now();
    final isMorning = now.hour >= 5 && now.hour < 12;
    final isEvening = now.hour >= 20 || now.hour < 5;
    final parts = isMorning
        ? _phrasesMorning
        : (isEvening ? _phrasesEvening : _phrasesDay);
    setState(() => phrase = parts[Random().nextInt(parts.length)]);
  }

  String _greeting() {
    final h = TimeOfDay.now().hour;
    if (h >= 5 && h < 12) return 'Доброе утро от Вселенной 🌞';
    if (h >= 20 || h < 5) return 'Спокойной ночи от Вселенной 🌙';
    return 'Тёплого дня от Вселенной ✨';
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Вселенная'), centerTitle: true, backgroundColor: const Color(0xFF6A4C93)),
      bottomNavigationBar: BottomNavigationBar(
        type: BottomNavigationBarType.fixed,
        items: const [
          BottomNavigationBarItem(icon: Icon(Icons.home), label: 'Домой'),
          BottomNavigationBarItem(icon: Icon(Icons.chat), label: 'Вселенная'),
          BottomNavigationBarItem(icon: Icon(Icons.favorite), label: 'Архив'),
          BottomNavigationBarItem(icon: Icon(Icons.settings), label: 'Настройки'),
        ],
        currentIndex: 0,
        onTap: (i) {
          if (i == 1) Navigator.pushNamed(context, '/ai');
          if (i == 2) Navigator.pushNamed(context, '/archive');
          if (i == 3) Navigator.pushNamed(context, '/settings');
        },
      ),
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            Text(_greeting(), style: const TextStyle(fontSize: 20, fontWeight: FontWeight.w600)),
            const SizedBox(height: 16),
            Expanded(
              child: CosmicAnimations.cosmicGlow(
                child: CosmicAnimations.floatingMessage(
                  child: Container(
                    padding: const EdgeInsets.all(20),
                    decoration: BoxDecoration(
                      color: Colors.white,
                      borderRadius: BorderRadius.circular(16),
                      boxShadow: [
                        BoxShadow(
                          color: const Color(0xFF6A4C93).withOpacity(0.2),
                          blurRadius: 20,
                          spreadRadius: 2,
                        ),
                      ],
                    ),
                    child: Center(
                      child: Text(
                        phrase,
                        textAlign: TextAlign.center,
                        style: const TextStyle(
                          fontSize: 20, 
                          fontStyle: FontStyle.italic,
                          fontWeight: FontWeight.w500,
                        ),
                      ),
                    ),
                  ),
                ),
              ),
            ),
            const SizedBox(height: 16),
            CosmicAnimations.pulsatingButton(
              child: ElevatedButton(
                onPressed: () => Navigator.pushNamed(context, '/mood'),
                style: ElevatedButton.styleFrom(
                  backgroundColor: const Color(0xFF6A4C93),
                  foregroundColor: Colors.white,
                  padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 16),
                  shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(25)),
                ),
                child: const Text('Как ты? 😊 😐 😞'),
              ),
            ),
            const SizedBox(height: 8),
            CosmicAnimations.pulsatingButton(
              child: ElevatedButton(
                onPressed: () => Navigator.pushNamed(context, '/send'),
                style: ElevatedButton.styleFrom(
                  backgroundColor: const Color(0xFF6A4C93),
                  foregroundColor: Colors.white,
                  padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 16),
                  shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(25)),
                ),
                child: const Text('Поделиться посланием от Вселенной 💌'),
              ),
            ),
            const SizedBox(height: 8),
            CosmicAnimations.pulsatingButton(
              child: ElevatedButton(
                onPressed: () => Navigator.pushNamed(context, '/ai'),
                style: ElevatedButton.styleFrom(
                  backgroundColor: const Color(0xFF6A4C93),
                  foregroundColor: Colors.white,
                  padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 16),
                  shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(25)),
                ),
                child: const Text('Поговорить с Вселенной 🌌'),
              ),
            ),
            const SizedBox(height: 8),
            CosmicAnimations.pulsatingButton(
              child: ElevatedButton(
                onPressed: () => Navigator.push(context, MaterialPageRoute(builder: (context) => const StatsScreen())),
                style: ElevatedButton.styleFrom(
                  backgroundColor: const Color(0xFF6A4C93),
                  foregroundColor: Colors.white,
                  padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 16),
                  shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(25)),
                ),
                child: const Text('Твоя статистика 📊'),
              ),
            ),
          ],
        ),
      ),
    );
  }
}

const _phrasesMorning = [
  'Вселенная верит в тебя! Сегодня будет отличный день! 🌟',
  'Ты можешь всё, что захочешь! Вселенная поддерживает тебя! ✨',
  'Доброе утро! Сегодня Вселенная приготовила для тебя чудеса! 🌈',
  'Звёзды выстроились в твою пользу! Сегодня всё получится! ⭐',
  'Вселенная создала этот день специально для тебя! 🌅',
  'Твоя энергия освещает весь мир! Продолжай сиять! ☀️',
  'Каждое утро - это новая возможность стать лучше! 🌱',
  'Вселенная обнимает тебя и желает удачного дня! 🤗',
];

const _phrasesDay = [
  'Вселенная шепчет: ты сильнее, чем думаешь! 💪',
  'Каждый момент - это подарок от Вселенной. Цени его! 🎁',
  'Вселенная создала тебя уникальным. Используй эту силу! 🌌',
  'Ты - часть чего-то большего! Твои действия важны! 🌠',
  'Вселенная направляет тебя к успеху! Следуй за мечтой! 🧭',
  'Каждая проблема - это возможность стать мудрее! 🌊',
  'Вселенная даёт тебе силы для любых свершений! 💎',
  'Твоя мечта - это компас Вселенной! Иди к ней смело! 🚀',
];

const _phrasesEvening = [
  'Вселенная гордится тобой! Ты сделал всё возможное! 🌙',
  'Спокойной ночи! Завтра Вселенная приготовит новые возможности! 🌠',
  'Отдыхай с миром! Ты заслужил покой и счастье! 💫',
  'Звёзды будут охранять твой сон! Сладких снов! ⭐',
  'Вселенная благодарит тебя за этот день! Ты молодец! 🌌',
  'Твои мечты сбудутся во сне! Позволь им расти! 🌈',
  'Вселенная обнимает тебя перед сном! Ты не один! 🤗',
  'Завтра будет ещё лучше! Вселенная уже готовит чудеса! 🌅',
];