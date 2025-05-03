(async () => {
    // Загрузка SVG-карты и CSV
    const [svgText, csvText] = await Promise.all([
      fetch('/static/map.svg').then(r => r.text()),
      fetch('/static/districts.csv').then(r => r.text())
    ]);
    document.getElementById('rf-map').innerHTML = svgText;
  
    // Парсим CSV: code → district_class
    const lines = csvText.trim().split('\n');
    const [header, ...rows] = lines.map(l => l.split(','));
    const idxCode  = header.indexOf('code');
    const idxClass = header.indexOf('district_class');
    const districtMap = {};
    rows.forEach(cols => {
      districtMap[cols[idxCode]] = cols[idxClass];
    });
  
    // Повесим обработчики на каждую область
    document.querySelectorAll('#rf-map svg path[data-code]').forEach(path => {
      const code = path.getAttribute('data-code');
      const cls  = districtMap[code];
      if (!cls) return;
      path.classList.add(`fd-${cls}`);
      path.dataset.districtClass = cls;
  
      // Подсветка при hover
      path.addEventListener('mouseenter', () => {
        document.querySelectorAll(
          `#rf-map svg path[data-district-class="${cls}"]`
        ).forEach(p => p.classList.add('highlight'));
      });
      path.addEventListener('mouseleave', () => {
        document.querySelectorAll(
          `#rf-map svg path[data-district-class="${cls}"]`
        ).forEach(p => p.classList.remove('highlight'));
      });
  
      // Клик — показать список языков
      path.addEventListener('click', async e => {
        e.stopPropagation();
        // снять старое
        const old = document.getElementById('language-list');
        if (old) old.remove();
  
        // запрос языков
        const res = await fetch(`/api/district-languages/${cls}`);
        if (!res.ok) return;
        const { name_ru, languages } = await res.json();
        if (!languages.length) return;
  
        // создаём окно
        const popup = document.createElement('div');
        popup.id = 'language-list';
        popup.style.left = (e.pageX + 10) + 'px';
        popup.style.top  = (e.pageY + 10) + 'px';
  
        const hdr = document.createElement('strong');
        hdr.textContent = name_ru + ' ФО';
        popup.appendChild(hdr);
  
        languages.forEach(item => {
          const el = document.createElement('div');
          el.textContent = item.language_name;
          el.addEventListener('click', () => {
            window.location.href = `/tasks/${item.language_id}`;
          });
          popup.appendChild(el);
        });
  
        document.body.appendChild(popup);
      });
    });
  
    // Клик вне — закрыть список и снять подсветку
    document.addEventListener('click', () => {
      const old = document.getElementById('language-list');
      if (old) old.remove();
      document.querySelectorAll('svg path.highlight')
        .forEach(p => p.classList.remove('highlight'));
    });
  })().catch(console.error);
  