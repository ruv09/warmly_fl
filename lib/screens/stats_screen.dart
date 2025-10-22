import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';
import '../widgets/cosmic_animations.dart';

class StatsScreen extends StatefulWidget {
  const StatsScreen({super.key});

  @override
  State<StatsScreen> createState() => _StatsScreenState();
}

class _StatsScreenState extends State<StatsScreen> {
  int _totalMessages = 0;
  int _aiConversations = 0;
  int _savedPhrases = 0;
  int _daysActive = 0;
  List<String> _achievements = [];

  @override
  void initState() {
    super.initState();
    _loadStats();
  }

  Future<void> _loadStats() async {
    final prefs = await SharedPreferences.getInstance();
    setState(() {
      _totalMessages = prefs.getInt('total_messages') ?? 0;
      _aiConversations = prefs.getInt('ai_conversations') ?? 0;
      _savedPhrases = prefs.getInt('saved_phrases') ?? 0;
      _daysActive = prefs.getInt('days_active') ?? 0;
      _achievements = prefs.getStringList('achievements') ?? [];
    });
  }

  Future<void> _addAchievement(String achievement) async {
    if (!_achievements.contains(achievement)) {
      setState(() {
        _achievements.add(achievement);
      });
      final prefs = await SharedPreferences.getInstance();
      await prefs.setStringList('achievements', _achievements);
      
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text('🎉 Новое достижение: $achievement'),
            backgroundColor: const Color(0xFF6A4C93),
          ),
        );
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return CosmicAnimations.cosmicBackground(
      child: Scaffold(
        backgroundColor: Colors.transparent,
        appBar: AppBar(
          title: const Text('Твоя Вселенная 📊'),
          backgroundColor: const Color(0xFF6A4C93),
          foregroundColor: Colors.white,
        ),
        body: SingleChildScrollView(
          padding: const EdgeInsets.all(16),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              // Статистика
              CosmicAnimations.cosmicGlow(
                child: Container(
                  padding: const EdgeInsets.all(20),
                  decoration: BoxDecoration(
                    color: Colors.white.withOpacity(0.1),
                    borderRadius: BorderRadius.circular(20),
                    border: Border.all(color: const Color(0xFF6A4C93).withOpacity(0.3)),
                  ),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      const Text(
                        'Твоя статистика',
                        style: TextStyle(
                          fontSize: 24,
                          fontWeight: FontWeight.bold,
                          color: Colors.white,
                        ),
                      ),
                      const SizedBox(height: 20),
                      _buildStatCard('Получено посланий от Вселенной', _totalMessages, '🌟'),
                      _buildStatCard('Разговоров с AI-агентом', _aiConversations, '🤖'),
                      _buildStatCard('Сохранённых фраз', _savedPhrases, '💾'),
                      _buildStatCard('Дней активности', _daysActive, '📅'),
                    ],
                  ),
                ),
              ),
              
              const SizedBox(height: 20),
              
              // Достижения
              CosmicAnimations.cosmicGlow(
                child: Container(
                  padding: const EdgeInsets.all(20),
                  decoration: BoxDecoration(
                    color: Colors.white.withOpacity(0.1),
                    borderRadius: BorderRadius.circular(20),
                    border: Border.all(color: const Color(0xFF6A4C93).withOpacity(0.3)),
                  ),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      const Text(
                        'Достижения',
                        style: TextStyle(
                          fontSize: 24,
                          fontWeight: FontWeight.bold,
                          color: Colors.white,
                        ),
                      ),
                      const SizedBox(height: 20),
                      if (_achievements.isEmpty)
                        const Text(
                          'Пока нет достижений. Продолжай общаться с Вселенной!',
                          style: TextStyle(color: Colors.white70),
                        )
                      else
                        ..._achievements.map((achievement) => Padding(
                          padding: const EdgeInsets.symmetric(vertical: 4),
                          child: Row(
                            children: [
                              const Icon(Icons.star, color: Colors.yellow, size: 20),
                              const SizedBox(width: 8),
                              Expanded(
                                child: Text(
                                  achievement,
                                  style: const TextStyle(color: Colors.white),
                                ),
                              ),
                            ],
                          ),
                        )),
                    ],
                  ),
                ),
              ),
              
              const SizedBox(height: 20),
              
              // Мотивационное сообщение
              CosmicAnimations.floatingMessage(
                child: CosmicAnimations.cosmicGlow(
                  child: Container(
                    padding: const EdgeInsets.all(20),
                    decoration: BoxDecoration(
                      color: const Color(0xFF6A4C93).withOpacity(0.2),
                      borderRadius: BorderRadius.circular(20),
                    ),
                    child: const Text(
                      'Вселенная гордится твоим прогрессом! 🌌\n\nКаждый день ты становишься лучше. Продолжай в том же духе!',
                      style: TextStyle(
                        fontSize: 16,
                        color: Colors.white,
                        fontStyle: FontStyle.italic,
                      ),
                      textAlign: TextAlign.center,
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

  Widget _buildStatCard(String title, int value, String emoji) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 8),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          Row(
            children: [
              Text(emoji, style: const TextStyle(fontSize: 20)),
              const SizedBox(width: 8),
              Text(
                title,
                style: const TextStyle(
                  color: Colors.white,
                  fontSize: 16,
                ),
              ),
            ],
          ),
          Text(
            value.toString(),
            style: const TextStyle(
              color: Colors.white,
              fontSize: 20,
              fontWeight: FontWeight.bold,
            ),
          ),
        ],
      ),
    );
  }
}