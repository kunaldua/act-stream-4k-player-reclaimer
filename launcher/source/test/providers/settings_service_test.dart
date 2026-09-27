/*
 * FLauncher
 * Copyright (C) 2021  Étienne Fesser
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 */

import 'package:flauncher/providers/settings_service.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:shared_preferences_platform_interface/shared_preferences_platform_interface.dart';

void main() {
  setUp(() {
    SharedPreferencesStorePlatform.instance =
        InMemorySharedPreferencesStore.empty();
  });

  test('setUse24HourTimeFormat', () async {
    final sharedPreferences = await SharedPreferences.getInstance();
    final settingsService = SettingsService(sharedPreferences);

    await settingsService.setUse24HourTimeFormat(false);

    expect(settingsService.use24HourTimeFormat, isFalse);
  });

  test('setAppHighlightAnimationEnabled', () async {
    final sharedPreferences = await SharedPreferences.getInstance();
    final settingsService = SettingsService(sharedPreferences);

    await settingsService.setAppHighlightAnimationEnabled(false);

    expect(settingsService.appHighlightAnimationEnabled, isFalse);
  });

  test('setGradientUuid', () async {
    final sharedPreferences = await SharedPreferences.getInstance();
    final settingsService = SettingsService(sharedPreferences);

    await settingsService
        .setGradientUuid('4730aa2d-1a90-49a6-9942-ffe82f470e26');

    expect(
        settingsService.gradientUuid, '4730aa2d-1a90-49a6-9942-ffe82f470e26');
  });

  group('setUnsplashAuthor', () {
    test('with value saves author info', () async {
      final sharedPreferences = await SharedPreferences.getInstance();
      final settingsService = SettingsService(sharedPreferences);

      await settingsService.setUnsplashAuthor('unsplash author');

      expect(settingsService.unsplashAuthor, 'unsplash author');
    });

    test('without value erases author info', () async {
      final sharedPreferences = await SharedPreferences.getInstance();
      await sharedPreferences.setString('unsplash_author', 'unsplash author');
      final settingsService = SettingsService(sharedPreferences);

      await settingsService.setUnsplashAuthor(null);

      expect(settingsService.unsplashAuthor, isNull);
    });
  });

  test('unsplash integration remains disabled without remote configuration',
      () async {
    final sharedPreferences = await SharedPreferences.getInstance();
    final settingsService = SettingsService(sharedPreferences);

    expect(settingsService.unsplashEnabled, isFalse);
  });
}
