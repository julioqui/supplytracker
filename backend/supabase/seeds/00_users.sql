-- 1️⃣ Tenants
INSERT INTO tenants (id, name, domain) VALUES 
('11111111-1111-1111-1111-111111111111', 'test-tenant', 'test.local');

-- 2️⃣ Roles (com tenant_id)
INSERT INTO roles (id, name, created_at) VALUES 
(1, 'admin', now()),
(2, 'user',  now());

-- 3️⃣ Users (com tenant_id)
INSERT INTO users (id, email, tenant_id, is_active, created_at) VALUES
('88c1e195-23ad-464b-839f-53da3875f077', 'teste@local.com', '11111111-1111-1111-1111-111111111111', TRUE, now());

-- 4️⃣ User ↔ Role relationship
INSERT INTO user_roles (user_id, role_id, created_at) VALUES
('88c1e195-23ad-464b-839f-53da3875f077', 1, now());
