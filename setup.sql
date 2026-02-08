-- Create tables and constraints

-- Resources Table
CREATE TABLE resources (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  title TEXT NOT NULL,
  type TEXT CHECK (type IN ('ppt', 'video')) NOT NULL,
  url TEXT NOT NULL,
  description TEXT,
  tags TEXT[], -- Array of text tags
  created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- Queries Table
CREATE TABLE queries (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  user_id UUID REFERENCES auth.users(id), -- Nullable for anonymous/mocked users if needed, or enforce auth
  query_text TEXT NOT NULL,
  response_json JSONB,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- RLS Policies

-- Enable RLS
ALTER TABLE resources ENABLE ROW LEVEL SECURITY;
ALTER TABLE queries ENABLE ROW LEVEL SECURITY;

-- Resources: Public Read Access (for learning content)
CREATE POLICY "Enable read access for all users" ON resources FOR SELECT USING (true);

-- Queries: Users can insert their own queries
-- If mocking auth, we might need a more permissive policy or just allow all inserts for the demo
CREATE POLICY "Enable insert for authenticated users only" ON queries FOR INSERT WITH CHECK (auth.uid() = user_id);

-- Queries: Users can view their own queries
CREATE POLICY "Enable select for users based on user_id" ON queries FOR SELECT USING (auth.uid() = user_id);


-- Seed Data (Sample Resources)
INSERT INTO resources (title, type, url, description, tags) VALUES
('Introduction to RAG', 'ppt', 'https://example.com/rag-intro.pptx', 'A basic introduction to Retrieval-Augmented Generation.', ARRAY['rag', 'ai', 'basics']),
('Advanced RAG Techniques', 'video', 'https://www.youtube.com/watch?v=example', 'Deep dive into RAG architectures.', ARRAY['rag', 'ai', 'advanced']),
('Supabase Overview', 'ppt', 'https://example.com/supabase.pptx', 'Getting started with Supabase.', ARRAY['database', 'supabase']);

-- STORAGE SETUP (Optional, requires storage extension enabled by default)
-- Create a public bucket for files
INSERT INTO storage.buckets (id, name, public)
VALUES ('content_files', 'content_files', true)
ON CONFLICT (id) DO NOTHING;

-- Policy: Public Read Access for storage
CREATE POLICY "Give public access to content_files" ON storage.objects
  FOR SELECT USING (bucket_id = 'content_files');

-- Policy: Allow authenticated uploads (or all for demo/setup simplicity)
CREATE POLICY "Allow uploads to content_files" ON storage.objects
  FOR INSERT WITH CHECK (bucket_id = 'content_files');
