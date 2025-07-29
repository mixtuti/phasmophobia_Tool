function updateList(id, items) {
  const ul = document.getElementById(id);
  ul.innerHTML = '';
  items.forEach(name => {
    const li = document.createElement('li');
    li.textContent = name;
    ul.appendChild(li);
  });
}

Promise.all([
  fetch('config.json').then(res => res.json()),
  fetch('ghost_output.json').then(res => res.json())
])
.then(([config, data]) => {
  document.body.style.fontSize = config.font_size + 'px';

  const candidates = document.getElementById('candidates');
  candidates.innerHTML = ''; // ←ここで初期化

  const limited = data.candidates.slice(0, config.max_ghosts);
  limited.forEach(name => {
    const li = document.createElement('li');
    li.textContent = name;
    li.style.minWidth = `${100 / config.columns}%`;
    candidates.appendChild(li);
  });

  const hiddenCount = data.candidates.length - limited.length;
  if (hiddenCount > 0) {
    const li = document.createElement('li');
    li.textContent = `他 ${hiddenCount} 種類`;
    li.style.opacity = 0.6;
    li.style.fontStyle = 'italic';
    li.style.minWidth = `${100 / config.columns}%`;
    candidates.appendChild(li);
  }

  updateList('selected', data.selected);
  updateList('excluded', data.excluded);
});
