USE Biotrace;

INSERT INTO file (type, name, content, created_at, updated_at, deleted_at) VALUES
('log', 'test_log1', '; test
[Files]
DataFolder=/path/to/data
TempFolder=/path/to/temp

[GUI]
WindowWidth=800
WindowHeight=600
Theme=Light

[Security]
APIKey=abc123xyz456', now(), now(), NULL),

('config', 'test_config1','; test
[Graphics]
Resolution=1920x1080
Quality=High

[Controls]
Sensitivity=5
InvertYAxis=false

[Audio]
MasterVolume=80
SoundEffectsVolume=70', now(), now(), NULL),

('log', 'test_log2', '; test
[Database]
DBName=RandomDB
DBHost=localhost
DBPort=3306

[Email]
SMTPServer=mail.example.com
SMTPPort=587

[Performance]
MaxThreads=4
CacheSize=256MB', now(), now(), NULL),

('config', 'test_config2','; test
[User]
Username=RandomUser
Language=English

[Display]
Theme=Dark
FontSize=12

[Security]
PasswordHash=2b5d7c3e2a1f8d9', now(), now(), NULL),

('config', 'test_config3','; test
[General]
AppName=RandomApp
Version=1.0

[Network]
ServerIP=192.168.1.1
Port=8080

[Logging]
LogLevel=Info
LogFile=app.log', now(), now(), NULL);

