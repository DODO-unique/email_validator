CREATE TABLE IF NOT EXISTS one_time_password (
    id SERIAL PRIMARY KEY,
    otp_id UUID UNIQUE,
    otp INT CHECK (
        otp > 1000 AND otp <= 9999
    ));

CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY,
    uname TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now());

CREATE TABLE IF NOT EXISTS running_sessions (
    id UUID PRIMARY KEY,
    user_id UUID UNIQUE NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    token UUID UNIQUE NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    expires_at TIMESTAMPTZ NOT NULL DEFAULT now() + INTERVAL '1 hour'
);