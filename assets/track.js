// BibleBucket real visitor counter via CountAPI
(function () {
  const NS = 'biblebucket-cosagax-v1'; // your unique namespace (keeps data separate)
  const page = 'page:' + encodeURIComponent(location.pathname || '/');

  // Increment global total counter
  fetch('https://api.countapi.xyz/hit/' + NS + '/total', { cache: 'no-store' }).catch(() => {});
  // Increment per-page counter
  fetch('https://api.countapi.xyz/hit/' + NS + '/' + page, { cache: 'no-store' }).catch(() => {});
})();
