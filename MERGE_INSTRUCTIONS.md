# Инструкции по завершению слияния

## ✅ Что уже сделано

1. ✅ GitHub Actions workflow исправлен:
   - Заменен `claude_code_oauth_token` на `github_token`
   - Добавлена поддержка `anthropic_api_key` и `claude_code_oauth_token`
   - Workflow временно отключен (`if: false`) до настройки API ключей
   - Обновлены права на `write` для pull-requests и issues

2. ✅ Изменения сохранены в ветке: `claude/merge-to-main-011CUqBrjjAyvLLLJpFAhKWh`

## 📋 Что нужно сделать вручную

### Шаг 1: Смержить исправления в main

Выполните одну из команд:

**Вариант A: Через GitHub UI (рекомендуется)**
1. Откройте: https://github.com/evgenygurin/rapperrok/compare/main...claude/merge-to-main-011CUqBrjjAyvLLLJpFAhKWh
2. Нажмите "Create pull request"
3. Смержите PR

**Вариант B: Локально**
```bash
git fetch origin
git checkout main
git merge origin/claude/merge-to-main-011CUqBrjjAyvLLLJpFAhKWh
git push origin main
```

### Шаг 2: Удалить старые ветки

После мержа в main, удалите старые ветки:

```bash
# Удалить все старые Claude ветки
git push origin --delete \
  claude/ai-music-api-docs-011CUq8LXxZefSUJCEEz41ap \
  claude/ai-music-api-docs-011CUq8M7TT9bm8PmvwaxUch \
  claude/ai-music-api-docs-011CUq8MsLQk6zokddTyiMYM \
  claude/ai-music-api-docs-011CUq8NdwYMYAxiYpz9uvtk \
  claude/merge-all-docs-011CUqAPNhGVES9fCGdAEJo2 \
  claude/fix-workflow-011CUqBrjjAyvLLLJpFAhKWh \
  claude/merge-to-main-011CUqBrjjAyvLLLJpFAhKWh
```

Или через GitHub UI:
1. Перейдите: https://github.com/evgenygurin/rapperrok/branches
2. Удалите каждую ветку `claude/*` вручную

### Шаг 3 (опционально): Включить Claude Code Review

Если хотите использовать автоматический code review:

1. Получите API ключ: https://console.anthropic.com/settings/keys
2. Добавьте секрет `ANTHROPIC_API_KEY`:
   - Перейдите: https://github.com/evgenygurin/rapperrok/settings/secrets/actions
   - Создайте новый секрет
3. Удалите строку `if: false` из `.github/workflows/claude-code-review.yml`

## 📝 Коммиты к мержу

- `99f8204` - fix: update Claude Code Review workflow to use GITHUB_TOKEN instead of OAuth token
- `e030ded` - fix: disable Claude Code Review workflow until API keys are configured

## 🎯 После завершения

После выполнения всех шагов:
- Workflow не будет падать с ошибками
- Старые ветки будут удалены
- Репозиторий будет чистым

---

*Этот файл можно удалить после завершения всех шагов*
