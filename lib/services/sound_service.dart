import 'package:audioplayers/audioplayers.dart';

class SoundService {
  static final SoundService _instance = SoundService._internal();
  factory SoundService() => _instance;
  SoundService._internal();

  final AudioPlayer _player = AudioPlayer();
  bool _isEnabled = true;

  Future<void> playNotificationSound() async {
    if (!_isEnabled) return;
    
    try {
      // Простой звук уведомления (можно заменить на космический звук)
      await _player.play(AssetSource('sounds/notification.mp3'));
    } catch (e) {
      // Если файл не найден, просто пропускаем
      print('Sound file not found: $e');
    }
  }

  Future<void> playAchievementSound() async {
    if (!_isEnabled) return;
    
    try {
      // Звук достижения
      await _player.play(AssetSource('sounds/achievement.mp3'));
    } catch (e) {
      print('Achievement sound file not found: $e');
    }
  }

  Future<void> playMessageSound() async {
    if (!_isEnabled) return;
    
    try {
      // Звук сообщения
      await _player.play(AssetSource('sounds/message.mp3'));
    } catch (e) {
      print('Message sound file not found: $e');
    }
  }

  Future<void> playCosmicSound() async {
    if (!_isEnabled) return;
    
    try {
      // Космический звук
      await _player.play(AssetSource('sounds/cosmic.mp3'));
    } catch (e) {
      print('Cosmic sound file not found: $e');
    }
  }

  void setEnabled(bool enabled) {
    _isEnabled = enabled;
  }

  bool get isEnabled => _isEnabled;

  Future<void> dispose() async {
    await _player.dispose();
  }
}