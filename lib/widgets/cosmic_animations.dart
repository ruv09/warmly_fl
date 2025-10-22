import 'package:flutter/material.dart';

class CosmicAnimations {
  static Widget twinklingStar({
    required Widget child,
    Duration duration = const Duration(seconds: 2),
  }) {
    return TweenAnimationBuilder<double>(
      duration: duration,
      tween: Tween(begin: 0.3, end: 1.0),
      builder: (context, value, child) {
        return Opacity(
          opacity: value,
          child: Transform.scale(
            scale: 0.8 + (value * 0.2),
            child: child,
          ),
        );
      },
      onEnd: () {
        // Анимация повторяется
      },
    );
  }

  static Widget floatingMessage({
    required Widget child,
    Duration duration = const Duration(seconds: 3),
  }) {
    return TweenAnimationBuilder<Offset>(
      duration: duration,
      tween: Tween(begin: const Offset(0, 0.1), end: const Offset(0, -0.1)),
      builder: (context, value, child) {
        return Transform.translate(
          offset: value,
          child: child,
        );
      },
    );
  }

  static Widget cosmicGlow({
    required Widget child,
    Color glowColor = const Color(0xFF6A4C93),
    double blurRadius = 20.0,
  }) {
    return Container(
      decoration: BoxDecoration(
        borderRadius: BorderRadius.circular(20),
        boxShadow: [
          BoxShadow(
            color: glowColor.withOpacity(0.3),
            blurRadius: blurRadius,
            spreadRadius: 2,
          ),
        ],
      ),
      child: child,
    );
  }

  static Widget pulsatingButton({
    required Widget child,
    Duration duration = const Duration(seconds: 1),
    double minScale = 0.95,
    double maxScale = 1.05,
  }) {
    return TweenAnimationBuilder<double>(
      duration: duration,
      tween: Tween(begin: minScale, end: maxScale),
      builder: (context, value, child) {
        return Transform.scale(
          scale: value,
          child: child,
        );
      },
      onEnd: () {
        // Анимация повторяется
      },
    );
  }

  static Widget cosmicBackground({
    required Widget child,
  }) {
    return Container(
      decoration: const BoxDecoration(
        gradient: LinearGradient(
          begin: Alignment.topLeft,
          end: Alignment.bottomRight,
          colors: [
            Color(0xFF1A1A2E),
            Color(0xFF16213E),
            Color(0xFF0F3460),
          ],
        ),
      ),
      child: child,
    );
  }

  static Widget starField({
    required Widget child,
  }) {
    return Stack(
      children: [
        // Фон со звёздами
        Container(
          decoration: const BoxDecoration(
            gradient: RadialGradient(
              center: Alignment.topLeft,
              radius: 1.0,
              colors: [
                Color(0xFF6A4C93),
                Color(0xFF1A1A2E),
              ],
            ),
          ),
        ),
        // Звёзды
        ...List.generate(50, (index) {
          return Positioned(
            left: (index * 37) % 400.0,
            top: (index * 23) % 800.0,
            child: twinklingStar(
              child: Container(
                width: 2,
                height: 2,
                decoration: const BoxDecoration(
                  color: Colors.white,
                  shape: BoxShape.circle,
                ),
              ),
            ),
          );
        }),
        child,
      ],
    );
  }
}