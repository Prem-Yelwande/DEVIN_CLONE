const chatMessages = document.getElementById('chat-messages');
const chatInput = document.getElementById('chat-input');
const sendBtn = document.getElementById('send-btn');
const resetBtn = document.getElementById('reset-btn');
const downloadBtn = document.getElementById('download-btn');
const previewFrame = document.getElementById('preview-frame');
const previewEmpty = document.getElementById('preview-empty');

let projectStarted = false;
let isLoading = false;

function addMessage(role, text, extraClass = '') {
  const emptyState = chatMessages.querySelector('.empty-state');
  if (emptyState) emptyState.remove();

  const div = document.createElement('div');
  div.className = `msg ${role} ${extraClass}`.trim();
  div.textContent = text;
  chatMessages.appendChild(div);
  chatMessages.scrollTop = chatMessages.scrollHeight;
  return div;
}

function refreshPreview() {
  const url = '/project/index.html?t=' + Date.now();
  fetch(url).then(res => {
    if (res.ok) {
      previewFrame.src = url;
      previewFrame.classList.remove('hidden');
      previewEmpty.classList.add('hidden');
    } else {
      previewFrame.classList.add('hidden');
      previewEmpty.classList.remove('hidden');
    }
  }).catch(() => {
    previewFrame.classList.add('hidden');
    previewEmpty.classList.remove('hidden');
  });
}

async function sendPrompt() {
  const text = chatInput.value.trim();
  if (!text || isLoading) return;

  addMessage('user', text);
  chatInput.value = '';
  chatInput.style.height = 'auto';
  isLoading = true;
  sendBtn.disabled = true;

  const loadingMsg = addMessage('assistant', projectStarted ? 'Applying changes...' : 'Building your app...', 'loading');

  try {
    const endpoint = projectStarted ? '/edit' : '/generate';
    const res = await fetch(endpoint, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ prompt: text })
    });
    const data = await res.json();

    loadingMsg.remove();

    if (data.status === 'done') {
      projectStarted = true;
      addMessage('assistant', 'Done.');
      refreshPreview();
    } else {
      addMessage('assistant', `Error: ${data.message || 'Something went wrong.'}`, 'error');
    }
  } catch (err) {
    loadingMsg.remove();
    addMessage('assistant', `Error: ${err.message}`, 'error');
  } finally {
    isLoading = false;
    sendBtn.disabled = false;
  }
}

sendBtn.addEventListener('click', sendPrompt);

chatInput.addEventListener('keydown', (e) => {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault();
    sendPrompt();
  }
});

chatInput.addEventListener('input', () => {
  chatInput.style.height = 'auto';
  chatInput.style.height = Math.min(chatInput.scrollHeight, 120) + 'px';
});

resetBtn.addEventListener('click', async () => {
  if (isLoading) return;
  await fetch('/reset', { method: 'POST' });
  projectStarted = false;
  chatMessages.innerHTML = '<div class="empty-state"><p>Describe what you want to build.</p></div>';
  previewFrame.classList.add('hidden');
  previewFrame.src = 'about:blank';
  previewEmpty.classList.remove('hidden');
});

downloadBtn.addEventListener('click', () => {
  window.location.href = '/download';
});

// On load, check if a project already exists
refreshPreview();