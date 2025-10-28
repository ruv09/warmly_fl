import 'dart:io';

import 'package:dotenv/dotenv.dart' as dotenv;
import 'package:teledart/teledart.dart';
import 'package:teledart/telegram.dart';

Future<void> main(List<String> args) async {
  // Load token from env or .env file
  dotenv.load();
  final token = Platform.environment['BOT_TOKEN'] ?? dotenv.env['BOT_TOKEN'];
  if (token == null || token.isEmpty) {
    stderr.writeln('BOT_TOKEN is not set. Set env or .env file.');
    exit(1);
  }

  final username = (await Telegram(token).getMe()).username;
  if (username == null) {
    stderr.writeln('Failed to fetch bot username. Check token.');
    exit(1);
  }

  final teledart = TeleDart(token, Event(username));
  await teledart.start();

  teledart.onCommand('start').listen((message) async {
    await teledart.telegram.sendMessage(
      message.chat.id,
      'Привет! Я бот warmly. Используй /help чтобы узнать команды.',
    );
  });

  teledart.onCommand('help').listen((message) async {
    await teledart.telegram.sendMessage(
      message.chat.id,
      '/start — приветствие\n/help — список команд\n/ping — проверить связь\n/mood — поделиться настроением',
    );
  });

  teledart.onCommand('ping').listen((message) async {
    await teledart.telegram.sendMessage(message.chat.id, 'pong');
  });

  teledart.onCommand('mood').listen((message) async {
    final text = message.text ?? '';
    final mood = text.replaceFirst(RegExp(r'^/mood\s*'), '').trim();
    if (mood.isEmpty) {
      await teledart.telegram.sendMessage(
        message.chat.id,
        'Какое у тебя настроение? Напиши так: /mood отлично',
      );
      return;
    }

    await teledart.telegram.sendMessage(
      message.chat.id,
      'Записал настроение: "$mood". Береги себя 💛',
    );
  });

  // Graceful shutdown
  ProcessSignal.sigint.watch().listen((_) async {
    await teledart.stop();
    exit(0);
  });
}
