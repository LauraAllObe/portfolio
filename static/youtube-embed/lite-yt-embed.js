/**
 * Ultra-optimized Lite YouTube Embed
 * For blazing-fast performance on portfolio/static sites
 */
class LiteYTEmbed extends HTMLElement {
  connectedCallback() {
    if (this.dataset.initialized) return;
    this.dataset.initialized = 'true';

    this.videoId = this.getAttribute('videoid');
    this.playLabel = this.getAttribute('playlabel') || 'Play';
    this.dataset.title = this.getAttribute('title') || '';

    this.style.backgroundImage = `url("https://i.ytimg.com/vi/${this.videoId}/hqdefault.jpg")`;
    this.style.backgroundPosition = 'center center';
    this.style.backgroundSize = 'cover';
    this.style.backgroundRepeat = 'no-repeat';
    this.upgradePosterImage();

    // Setup play button
    const btn = document.createElement('button');
    btn.type = 'button';
    btn.className = 'lyt-playbtn';
    const span = document.createElement('span');
    span.className = 'lyt-visually-hidden';
    span.textContent = this.playLabel;
    btn.append(span);
    this.append(btn);

    // A11y keyboard interaction fallback
    btn.addEventListener('keydown', e => {
      if (e.key === 'Enter' || e.key === ' ') {
        e.preventDefault();
        this.activate();
      }
    });

    // Prefetch resources
    this.addEventListener('pointerover', LiteYTEmbed.warmConnections, { once: true });
    this.addEventListener('focusin', LiteYTEmbed.warmConnections, { once: true });

    // Load real iframe on interaction
    this.addEventListener('click', this.activate.bind(this));

    // Safari/iOS autoplay workaround
    this.needsYTApi = this.hasAttribute("js-api") || navigator.vendor.includes('Apple') || navigator.userAgent.includes('Mobi');

    // Defer SEO noscript iframe
    if ('requestIdleCallback' in window) {
      requestIdleCallback(() => this.addNoscriptIframe());
    } else {
      setTimeout(() => this.addNoscriptIframe(), 300);
    }
  }

  static warmConnections() {
    if (LiteYTEmbed.preconnected) return;
    LiteYTEmbed.preconnected = true;
    [
      'https://www.youtube-nocookie.com',
      'https://i.ytimg.com'
    ].forEach(href => {
      const link = document.createElement('link');
      link.rel = 'preconnect';
      link.href = href;
      document.head.append(link);
    });
  }

  getParams() {
    const params = new URLSearchParams(this.getAttribute('params') || []);
    params.set('autoplay', '1');
    params.set('playsinline', '1');
    return params;
  }

  async activate() {
    if (this.classList.contains('lyt-activated')) return;
    this.classList.add('lyt-activated');

    if (this.needsYTApi) {
      return this.addYTPlayerIframe();
    }

    const iframe = this.createBasicIframe();
    this.append(iframe);
    iframe.focus();
  }

  createBasicIframe() {
    const iframe = document.createElement('iframe');
    iframe.width = 560;
    iframe.height = 315;
    iframe.loading = 'lazy';
    iframe.title = this.playLabel;
    iframe.allow = 'accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture';
    iframe.allowFullscreen = true;
    iframe.src = `https://www.youtube-nocookie.com/embed/${encodeURIComponent(this.videoId)}?${this.getParams().toString()}`;
    iframe.style.width = '100%';
    iframe.style.height = '100%';
    iframe.style.border = '0';
    iframe.style.position = 'absolute';
    iframe.style.top = '0';
    iframe.style.left = '0';
    return iframe;
  }

  async addYTPlayerIframe() {
    if (window.YT && window.YT.Player) return;

    this.ytApiPromise = new Promise((resolve, reject) => {
      const script = document.createElement('script');
      script.src = 'https://www.youtube.com/iframe_api';
      script.async = true;
      script.onload = () => YT.ready(resolve);
      script.onerror = reject;
      document.head.append(script);
    });

    await this.ytApiPromise;

    const placeholder = document.createElement('div');
    this.append(placeholder);

    this.playerPromise = new Promise(resolve => {
      const player = new YT.Player(placeholder, {
        width: '100%',
        videoId: this.videoId,
        playerVars: Object.fromEntries(this.getParams().entries()),
        events: {
          'onReady': event => {
            event.target.playVideo();
            resolve(player);
          }
        }
      });
    });
  }

  addNoscriptIframe() {
    const iframe = this.createBasicIframe();
    const noscript = document.createElement('noscript');
    noscript.innerHTML = iframe.outerHTML;
    this.append(noscript);
  }

  upgradePosterImage() {
    setTimeout(() => {
      const url = `https://i.ytimg.com/vi_webp/${this.videoId}/sddefault.webp`;
      const img = new Image();
      img.fetchPriority = 'low';
      img.referrerPolicy = 'origin';
      img.src = url;
      img.onload = e => {
        const bad = e.target.naturalHeight === 90 && e.target.naturalWidth === 120;
        if (!bad) {
          this.style.backgroundImage = `url("${url}")`;
        }
      };
    }, 100);
  }
}

customElements.define('lite-youtube', LiteYTEmbed);