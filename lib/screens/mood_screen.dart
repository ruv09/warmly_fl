import 'dart:math';
import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';

class MoodScreen extends StatefulWidget {
  const MoodScreen({super.key});

  @override
  State<MoodScreen> createState() => _MoodScreenState();
}

class _MoodScreenState extends State<MoodScreen> {
  String? mood; // good | ok | bad
  String? phrase;

  Future<void> _saveFavorite(String text) async {
    final prefs = await SharedPreferences.getInstance();
    final list = prefs.getStringList('favorites') ?? [];
    list.add('${DateTime.now().toIso8601String()}|$text');
    await prefs.setStringList('favorites', list);
    if (mounted) Navigator.pop(context);
  }

  void pickPhrase(String m) {
    final pool = m == 'good' ? _phrasesGood : (m == 'ok' ? _phrasesOk : _phrasesBad);
    setState(() {
      mood = m;
      phrase = pool[Random().nextInt(pool.length)];
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Как ты себя чувствуешь?'), backgroundColor: const Color(0xFF6A4C93)),
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            Wrap(
              spacing: 12,
              children: [
                ChoiceChip(label: const Text('😊 Хорошо'), selected: mood=='good', onSelected: (_) => pickPhrase('good')),
                ChoiceChip(label: const Text('😐 Нормально'), selected: mood=='ok', onSelected: (_) => pickPhrase('ok')),
                ChoiceChip(label: const Text('😞 Плохо'), selected: mood=='bad', onSelected: (_) => pickPhrase('bad')),
              ],
            ),
            const SizedBox(height: 16),
            if (phrase != null)
              Expanded(
                child: Container(
                  padding: const EdgeInsets.all(20),
                  decoration: BoxDecoration(color: Colors.white, borderRadius: BorderRadius.circular(16)),
                  child: Center(
                    child: Text(phrase!, textAlign: TextAlign.center, style: const TextStyle(fontSize: 20, fontStyle: FontStyle.italic)),
                  ),
                ),
              ),
            const SizedBox(height: 16),
            if (phrase != null)
              ElevatedButton(onPressed: () => _saveFavorite(phrase!), child: const Text('Сохранить в архив ❤️')),
            TextButton(onPressed: () => Navigator.pop(context), child: const Text('Пропустить')),
          ],
        ),
      ),
    );
  }
}

const _phrasesGood = [
  'Вселенная радуется вместе с тобой! 🌟',
  'Твоя радость освещает весь мир! ✨',
  'Продолжай сиять - ты вдохновляешь других! 🌈',
];

const _phrasesOk = [
  'Вселенная понимает тебя. Нормально - это тоже нормально.',
  'Каждый день - это новый шанс. Ты на правильном пути! 🌱',
  'Вселенная терпелива. Ты тоже можешь быть терпеливым к себе.',
];

const _phrasesBad = [
  'Вселенная обнимает тебя в трудные моменты. Ты не один! 🤗',
  'Даже в темноте звезды светят ярче. Ты - одна из них! ⭐',
  'Вселенная верит в тебя, даже когда ты не веришь в себя. 💫',
];