import 'dart:math';
import 'package:flutter/material.dart';
import 'package:share_plus/share_plus.dart';

class SendScreen extends StatefulWidget {
  const SendScreen({super.key});

  @override
  State<SendScreen> createState() => _SendScreenState();
}

class _SendScreenState extends State<SendScreen> {
  late List<String> pool;
  @override
  void initState() {
    super.initState();
    pool = List.of(_friendPhrases)..shuffle(Random());
  }

  void sharePhrase(String text) {
    final message = 'Тебе прислали послание от Вселенной 🌌\n"$text"\n— via Вселенная';
    Share.share(message);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Поделись посланием от Вселенной'), backgroundColor: const Color(0xFF6A4C93)),
      body: ListView.builder(
        padding: const EdgeInsets.all(16),
        itemCount: min(5, pool.length),
        itemBuilder: (context, i) {
          final text = pool[i];
          return Card(
            child: ListTile(
              title: Text(text),
              trailing: TextButton(onPressed: () => sharePhrase(text), child: const Text('Отправить')), 
            ),
          );
        },
      ),
    );
  }
}

const _friendPhrases = [
  'Вселенная верит в тебя! Ты можешь всё! 🌟',
  'Ты - звезда во Вселенной! Сияй ярче! ✨',
  'Вселенная создала тебя особенным. Помни об этом! 🌌',
  'Каждый день - это подарок от Вселенной. Цени его! 🎁',
  'Вселенная обнимает тебя в трудные моменты! 🤗',
];