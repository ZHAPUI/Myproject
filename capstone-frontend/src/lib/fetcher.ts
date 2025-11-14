// src/lib/fetcher.ts
import { Story } from './types';

// 动态获取 API 地址，支持跨设备访问
// 如果当前是 localhost，就用 localhost:8888
// 否则使用当前主机名（适合同一局域网内的其他设备访问）
const getApiBaseUrl = () => {
  const isLocalhost =
    window.location.hostname === 'localhost' ||
    window.location.hostname === '127.0.0.1';

  if (isLocalhost) {
    // 本地开发：连你本机 8888 端口
    return 'http://localhost:8888';
  }

  // 线上环境（GitHub Pages 等）：连 Render 后端
  return 'https://myproject-pkrn.onrender.com';
};

const API_BASE_URL = getApiBaseUrl();

export async function fetchStory(): Promise<Story> {
  try {
    // 优先从后端数据库获取
    const response = await fetch(`${API_BASE_URL}/story`);
    
    if (response.ok) {
      const story: Story = await response.json();
      console.log('✓ Story loaded from database');
      return story;
    }
    
    // 如果数据库没有数据，回退到本地 story.json
    console.log('⚠ Database empty, falling back to local story.json');
    const fallbackResponse = await fetch('/story.json');
    
    if (!fallbackResponse.ok) {
      throw new Error(`HTTP error! status: ${fallbackResponse.status}`);
    }
    
    const story: Story = await fallbackResponse.json();
    return story;
  } catch (error) {
    console.error('Failed to fetch story:', error);
    throw error;
  }
}