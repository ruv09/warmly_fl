import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'package:shared_preferences/shared_preferences.dart';
import '../widgets/cosmic_animations.dart';
import '../services/sound_service.dart';

class AiChatScreen extends StatefulWidget {
  const AiChatScreen({super.key});

  @override
  State<AiChatScreen> createState() => _AiChatScreenState();
}

class _AiChatScreenState extends State<AiChatScreen> {
  final TextEditingController _messageController = TextEditingController();
  final List<ChatMessage> _messages = [];
  bool _isLoading = false;

  @override
  void initState() {
    super.initState();
    _addWelcomeMessage();
  }

  void _addWelcomeMessage() {
    _messages.add(ChatMessage(
      text: "Привет! Я Вселенная 🌌\n\nЯ здесь, чтобы подбадривать тебя и помогать принимать решения. Задавай любые вопросы - я всегда на твоей стороне!",
      isUser: false,
      timestamp: DateTime.now(),
    ));
  }

  Future<void> _sendMessage() async {
    final text = _messageController.text.trim();
    if (text.isEmpty) return;

    setState(() {
      _messages.add(ChatMessage(
        text: text,
        isUser: true,
        timestamp: DateTime.now(),
      ));
      _isLoading = true;
    });

    _messageController.clear();

    // Обновляем статистику
    await _updateStats();

    // Воспроизводим звук сообщения
    SoundService().playMessageSound();

    try {
      final response = await _getAiResponse(text);
      setState(() {
        _messages.add(ChatMessage(
          text: response,
          isUser: false,
          timestamp: DateTime.now(),
        ));
        _isLoading = false;
      });
    } catch (e) {
      setState(() {
        _messages.add(ChatMessage(
          text: "Извини, у меня сейчас технические проблемы. Но помни - ты сильнее, чем думаешь! 💪",
          isUser: false,
          timestamp: DateTime.now(),
        ));
        _isLoading = false;
      });
    }
  }

  Future<void> _updateStats() async {
    final prefs = await SharedPreferences.getInstance();
    final totalMessages = (prefs.getInt('total_messages') ?? 0) + 1;
    final aiConversations = (prefs.getInt('ai_conversations') ?? 0) + 1;
    
    await prefs.setInt('total_messages', totalMessages);
    await prefs.setInt('ai_conversations', aiConversations);
    
    // Проверяем достижения
    if (aiConversations == 1) {
      await _addAchievement('Первое общение с Вселенной 🌟');
    } else if (aiConversations == 10) {
      await _addAchievement('10 разговоров с Вселенной 🚀');
    } else if (aiConversations == 50) {
      await _addAchievement('50 разговоров с Вселенной 🌌');
    } else if (aiConversations == 100) {
      await _addAchievement('100 разговоров с Вселенной ⭐');
    }
  }

  Future<void> _addAchievement(String achievement) async {
    final prefs = await SharedPreferences.getInstance();
    final achievements = prefs.getStringList('achievements') ?? [];
    if (!achievements.contains(achievement)) {
      achievements.add(achievement);
      await prefs.setStringList('achievements', achievements);
      
      if (mounted) {
        // Воспроизводим звук достижения
        SoundService().playAchievementSound();
        
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text('🎉 Новое достижение: $achievement'),
            backgroundColor: const Color(0xFF6A4C93),
          ),
        );
      }
    }
  }

  Future<String> _getAiResponse(String userMessage) async {
    // Простая имитация AI-ответов с мотивационными сообщениями
    await Future.delayed(const Duration(seconds: 1));
    
    final responses = [
      "Вселенная верит в тебя! 🌟 Каждый шаг, который ты делаешь, приближает тебя к твоим целям. Не думай - действуй!",
      "Ты сильнее, чем думаешь! 💪 Помни: Вселенная создала тебя уникальным. Используй эту силу!",
      "Не сомневайся в себе! ✨ Ты уже прошёл через столько трудностей - значит, справишься и с этим.",
      "Принимай решения смело! 🚀 Вселенная поддерживает тебя. Доверяй своей интуиции.",
      "Ты не один! 🌌 Вселенная всегда рядом. Каждая проблема - это возможность стать лучше.",
      "Верь в себя! 💫 Ты достоин всего самого лучшего. Не позволяй страхам останавливать тебя.",
      "Действуй! 🎯 Не жди идеального момента - он уже наступил. Ты готов к любым вызовам.",
      "Ты можешь всё! 🌈 Вселенная дала тебе все необходимые качества. Просто используй их!",
      "Звёзды светят ярче всего в темноте! ⭐ Твоя сила проявляется в трудные моменты.",
      "Вселенная создала тебя для великих дел! 🌌 Не ограничивай себя сомнениями.",
      "Каждый день - это новая возможность! 🌅 Вселенная даёт тебе шанс стать лучше.",
      "Ты - часть чего-то большего! 🌠 Твои действия влияют на весь мир вокруг.",
      "Вселенная шепчет тебе: 'Ты готов!' 🌙 Слушай свой внутренний голос.",
      "Не бойся ошибаться! 🌊 Ошибки - это звёзды, которые ведут к успеху.",
      "Твоя мечта - это компас Вселенной! 🧭 Следуй за ней смело.",
      "Вселенная обнимает тебя! 🤗 Ты в безопасности, даже когда страшно.",
      "Ты - чудо! ✨ Вселенная потратила миллиарды лет, чтобы создать именно тебя.",
      "Не сравнивай себя с другими! 🌸 Ты уникален, как каждая звезда на небе.",
      "Вселенная ждёт твоего следующего шага! 🚀 Что ты сделаешь сегодня?",
      "Твоя сила безгранична! 💎 Вселенная вложила в тебя всё необходимое.",
    ];

    // Улучшенная логика выбора ответа на основе ключевых слов
    final message = userMessage.toLowerCase();
    
    if (message.contains('как') || message.contains('что делать') || message.contains('помоги')) {
      return "Не думай, а делай! 🚀 Вселенная говорит: принимай решения четко и ясно. Ты уже знаешь ответ - просто доверься себе!";
    } else if (message.contains('страх') || message.contains('боюсь') || message.contains('страшно')) {
      return "Страх - это нормально! 💪 Но помни: за страхом скрывается твоя сила. Вселенная верит в тебя - поверь и ты!";
    } else if (message.contains('не могу') || message.contains('не получается') || message.contains('не умею')) {
      return "Ты МОЖЕШЬ! 🌟 Каждый раз, когда ты говоришь 'не могу', Вселенная шепчет: 'Попробуй еще раз'. Ты сильнее своих сомнений!";
    } else if (message.contains('устал') || message.contains('устала') || message.contains('усталость')) {
      return "Отдых - это тоже достижение! 🌙 Вселенная говорит: ты уже сделал достаточно. Позволь себе передохнуть и набраться сил.";
    } else if (message.contains('грустно') || message.contains('грусть') || message.contains('печально')) {
      return "Грусть - это тоже часть жизни! 🌧️ Вселенная обнимает тебя в трудные моменты. Завтра будет лучше, а сегодня - просто будь с собой.";
    } else if (message.contains('один') || message.contains('одиноко') || message.contains('одиночество')) {
      return "Ты не один! 🌌 Вселенная всегда рядом. Миллиарды звёзд светят для тебя. Ты часть огромного космоса!";
    } else if (message.contains('любовь') || message.contains('любить') || message.contains('сердце')) {
      return "Любовь - это сила Вселенной! 💖 Ты достоин любви и счастья. Начни с любви к себе - остальное приложится.";
    } else if (message.contains('работа') || message.contains('карьера') || message.contains('успех')) {
      return "Вселенная создала тебя для великих дел! 🏆 Твоя работа - это способ изменить мир к лучшему. Верь в свои способности!";
    } else if (message.contains('будущее') || message.contains('завтра') || message.contains('план')) {
      return "Будущее в твоих руках! 🔮 Вселенная даёт тебе возможность создавать свою реальность. Каждый день - это новый шанс!";
    } else if (message.contains('спасибо') || message.contains('благодарю')) {
      return "Пожалуйста! 🌟 Вселенная рада помочь тебе. Ты делаешь мир лучше, просто будучи собой!";
    } else if (message.contains('привет') || message.contains('здравствуй') || message.contains('hi')) {
      return "Привет! 🌌 Добро пожаловать во Вселенную! Я здесь, чтобы поддержать тебя. Как дела?";
    } else if (message.contains('пока') || message.contains('до свидания') || message.contains('bye')) {
      return "До встречи! 🌙 Вселенная всегда с тобой. Возвращайся, когда захочешь поговорить!";
    } else {
      return responses[DateTime.now().millisecond % responses.length];
    }
  }

  @override
  Widget build(BuildContext context) {
    return CosmicAnimations.cosmicBackground(
      child: Scaffold(
        backgroundColor: Colors.transparent,
        appBar: AppBar(
          title: const Text('Чат с Вселенной 🌌'),
          backgroundColor: const Color(0xFF6A4C93),
          foregroundColor: Colors.white,
        ),
      body: Column(
        children: [
          Expanded(
            child: ListView.builder(
              padding: const EdgeInsets.all(16),
              itemCount: _messages.length + (_isLoading ? 1 : 0),
              itemBuilder: (context, index) {
                if (index == _messages.length && _isLoading) {
                  return const Padding(
                    padding: EdgeInsets.all(16),
                    child: Center(
                      child: CircularProgressIndicator(),
                    ),
                  );
                }
                return _buildMessage(_messages[index]);
              },
            ),
          ),
          Container(
            padding: const EdgeInsets.all(16),
            decoration: BoxDecoration(
              color: Colors.white,
              boxShadow: [
                BoxShadow(
                  color: Colors.grey.withOpacity(0.2),
                  spreadRadius: 1,
                  blurRadius: 5,
                  offset: const Offset(0, -3),
                ),
              ],
            ),
            child: Row(
              children: [
                Expanded(
                  child: TextField(
                    controller: _messageController,
                    decoration: const InputDecoration(
                      hintText: 'Напиши Вселенной...',
                      border: OutlineInputBorder(
                        borderRadius: BorderRadius.all(Radius.circular(25)),
                      ),
                      contentPadding: EdgeInsets.symmetric(horizontal: 16, vertical: 12),
                    ),
                    onSubmitted: (_) => _sendMessage(),
                  ),
                ),
                const SizedBox(width: 8),
                FloatingActionButton(
                  onPressed: _isLoading ? null : _sendMessage,
                  backgroundColor: const Color(0xFF6A4C93),
                  child: const Icon(Icons.send, color: Colors.white),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildMessage(ChatMessage message) {
    return CosmicAnimations.floatingMessage(
      child: Padding(
        padding: const EdgeInsets.symmetric(vertical: 4),
        child: Row(
          mainAxisAlignment: message.isUser ? MainAxisAlignment.end : MainAxisAlignment.start,
          children: [
            if (!message.isUser) ...[
              CosmicAnimations.twinklingStar(
                child: CircleAvatar(
                  radius: 16,
                  backgroundColor: const Color(0xFF6A4C93),
                  child: const Text('🌌', style: TextStyle(fontSize: 16)),
                ),
              ),
              const SizedBox(width: 8),
            ],
            Flexible(
              child: CosmicAnimations.cosmicGlow(
                child: Container(
                  padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
                  decoration: BoxDecoration(
                    color: message.isUser 
                        ? const Color(0xFF6A4C93) 
                        : Colors.grey[100],
                    borderRadius: BorderRadius.circular(20),
                  ),
                  child: Text(
                    message.text,
                    style: TextStyle(
                      color: message.isUser ? Colors.white : Colors.black87,
                      fontSize: 16,
                    ),
                  ),
                ),
              ),
            ),
            if (message.isUser) ...[
              const SizedBox(width: 8),
              CircleAvatar(
                radius: 16,
                backgroundColor: Colors.grey[300],
                child: const Icon(Icons.person, size: 16, color: Colors.white),
              ),
            ],
          ],
        ),
      ),
    );
  }

  @override
  void dispose() {
    _messageController.dispose();
    super.dispose();
  }
}

class ChatMessage {
  final String text;
  final bool isUser;
  final DateTime timestamp;

  ChatMessage({
    required this.text,
    required this.isUser,
    required this.timestamp,
  });
}