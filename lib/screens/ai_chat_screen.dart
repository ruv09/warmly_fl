import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

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
    ];

    // Простая логика выбора ответа на основе ключевых слов
    if (userMessage.toLowerCase().contains('как') || userMessage.toLowerCase().contains('что делать')) {
      return "Не думай, а делай! 🚀 Вселенная говорит: принимай решения четко и ясно. Ты уже знаешь ответ - просто доверься себе!";
    } else if (userMessage.toLowerCase().contains('страх') || userMessage.toLowerCase().contains('боюсь')) {
      return "Страх - это нормально! 💪 Но помни: за страхом скрывается твоя сила. Вселенная верит в тебя - поверь и ты!";
    } else if (userMessage.toLowerCase().contains('не могу') || userMessage.toLowerCase().contains('не получается')) {
      return "Ты МОЖЕШЬ! 🌟 Каждый раз, когда ты говоришь 'не могу', Вселенная шепчет: 'Попробуй еще раз'. Ты сильнее своих сомнений!";
    } else if (userMessage.toLowerCase().contains('устал') || userMessage.toLowerCase().contains('устала')) {
      return "Отдых - это тоже достижение! 🌙 Вселенная говорит: ты уже сделал достаточно. Позволь себе передохнуть и набраться сил.";
    } else {
      return responses[DateTime.now().millisecond % responses.length];
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
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
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 4),
      child: Row(
        mainAxisAlignment: message.isUser ? MainAxisAlignment.end : MainAxisAlignment.start,
        children: [
          if (!message.isUser) ...[
            CircleAvatar(
              radius: 16,
              backgroundColor: const Color(0xFF6A4C93),
              child: const Text('🌌', style: TextStyle(fontSize: 16)),
            ),
            const SizedBox(width: 8),
          ],
          Flexible(
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