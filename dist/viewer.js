fetch('ghost_output.json')
  .then(response => response.json())
  .then(data => {
    fetch('config.json')
      .then(response => response.json())
      .then(config => {
        document.body.style.fontSize = config.font_size + 'px';

        const selected = document.getElementById('selected');
        const excluded = document.getElementById('excluded');
        const candidates = document.getElementById('candidates');

        // リスト初期化
        selected.innerHTML = '';
        excluded.innerHTML = '';
        candidates.innerHTML = '';

        data.selected.forEach(name => {
          const li = document.createElement('li');
          li.textContent = name;
          selected.appendChild(li);
        });

        data.excluded.forEach(name => {
          const li = document.createElement('li');
          li.textContent = name;
          excluded.appendChild(li);
        });

        const max = config.max_ghosts;
        const shown = data.candidates.slice(0, max);

        shown.forEach(name => {
          const li = document.createElement('li');
          li.textContent = name;
          li.style.minWidth = `${100 / config.columns}%`;
          candidates.appendChild(li);
        });

        const remaining = data.candidates.length - max;
        if (remaining > 0) {
          const li = document.createElement('li');
          li.textContent = `他${remaining}種類`;
          li.style.opacity = 0.5;
          li.style.fontStyle = 'italic';
          li.style.minWidth = `${100 / config.columns}%`;
          candidates.appendChild(li);
        }
      });
  });
