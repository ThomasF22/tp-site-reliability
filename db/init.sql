-- Script d'initialisation de la base de données forum
-- Ce script sera exécuté automatiquement au démarrage du conteneur

USE forum_db;

-- Table des utilisateurs
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    display_name VARCHAR(100) NOT NULL,
    bio TEXT,
    avatar_url VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    INDEX idx_username (username),
    INDEX idx_email (email)
);

-- Table des posts
CREATE TABLE posts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    content TEXT NOT NULL,
    image_url VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id),
    INDEX idx_created_at (created_at)
);

-- Table des commentaires
CREATE TABLE comments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    post_id INT NOT NULL,
    user_id INT NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (post_id) REFERENCES posts(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_post_id (post_id),
    INDEX idx_user_id (user_id),
    INDEX idx_created_at (created_at)
);

-- Table des likes pour les posts
CREATE TABLE post_likes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    post_id INT NOT NULL,
    user_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (post_id) REFERENCES posts(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    UNIQUE KEY unique_post_like (post_id, user_id),
    INDEX idx_post_id (post_id),
    INDEX idx_user_id (user_id)
);

-- Table des likes pour les commentaires
CREATE TABLE comment_likes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    comment_id INT NOT NULL,
    user_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (comment_id) REFERENCES comments(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    UNIQUE KEY unique_comment_like (comment_id, user_id),
    INDEX idx_comment_id (comment_id),
    INDEX idx_user_id (user_id)
);

-- Table des sessions pour l'authentification
CREATE TABLE user_sessions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    session_id VARCHAR(255) UNIQUE NOT NULL,
    user_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_session_id (session_id),
    INDEX idx_user_id (user_id),
    INDEX idx_expires_at (expires_at)
);

-- Vue pour compter les likes des posts
CREATE VIEW post_like_counts AS
SELECT 
    post_id,
    COUNT(*) as like_count
FROM post_likes 
GROUP BY post_id;

-- Vue pour compter les likes des commentaires
CREATE VIEW comment_like_counts AS
SELECT 
    comment_id,
    COUNT(*) as like_count
FROM comment_likes 
GROUP BY comment_id;

-- Vue pour compter les commentaires par post
CREATE VIEW post_comment_counts AS
SELECT 
    post_id,
    COUNT(*) as comment_count
FROM comments 
GROUP BY post_id;

-- Insertion de données de test
INSERT INTO users (username, email, password_hash, display_name, bio) VALUES
('john_doe', 'john@example.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj0kEGg0OP22', 'John Doe', 'Développeur passionné'),
('jane_smith', 'jane@example.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj0kEGg0OP22', 'Jane Smith', 'Designer créative'),
('bob_wilson', 'bob@example.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj0kEGg0OP22', 'Bob Wilson', 'Admin du forum');

-- Insertion de posts de test
INSERT INTO posts (user_id, content) VALUES
(1, 'Bonjour tout le monde! Premier post sur ce nouveau forum 🚀'),
(2, 'Super interface! J''adore le design épuré. Félicitations à l''équipe! 🎨'),
(3, 'Bienvenue sur notre forum Twitter-like! N''hésitez pas à partager vos idées 💡'),
(1, 'Test de posting avec un contenu plus long... Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.');

-- Insertion de commentaires de test  
INSERT INTO comments (post_id, user_id, content) VALUES
(1, 2, 'Bienvenue John! Hâte de voir tes prochains posts 👍'),
(1, 3, 'Excellent premier post! '),
(2, 1, 'Merci Jane! Le design est vraiment réussi'),
(3, 2, 'Merci pour l''accueil! 😊');

-- Insertion de likes de test
INSERT INTO post_likes (post_id, user_id) VALUES
(1, 2), (1, 3),
(2, 1), (2, 3),
(3, 1), (3, 2);

INSERT INTO comment_likes (comment_id, user_id) VALUES
(1, 1), (1, 3),
(2, 1),
(3, 2),
(4, 1), (4, 3);

-- Afficher un résumé de la base initialisée
SELECT 'Base de données forum_db initialisée avec succès!' as status;
SELECT 
    (SELECT COUNT(*) FROM users) as nb_users,
    (SELECT COUNT(*) FROM posts) as nb_posts,
    (SELECT COUNT(*) FROM comments) as nb_comments,
    (SELECT COUNT(*) FROM post_likes) as nb_post_likes,
    (SELECT COUNT(*) FROM comment_likes) as nb_comment_likes;