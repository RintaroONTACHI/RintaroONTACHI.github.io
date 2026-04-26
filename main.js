let auth0Client = null;

// Auth0の設定
const config = {
  domain: "epsilon.jp.auth0.com", // Auth0ダッシュボードからコピーしてください
  clientId: "TQ8auFHVhAe44FtxkoOhUPyWScIOXIMI"   // Auth0ダッシュボードからコピーしてください
};

window.onload = async () => {
  auth0Client = await createAuth0Client({
    domain: config.domain,
    clientId: config.clientId,
    authorizationParams: {
      // 画像の設定「許可するCallback URL」に合わせる
      redirect_uri: "https://rintaroontachi.github.io/ok"
    }
  });

  // 現在のページが /ok (コールバックURL) の場合、認証処理を実行
  if (window.location.pathname.endsWith("/ok")) {
    try {
      await auth0Client.handleRedirectCallback();
      // 認証が終わったらトップページへ
      window.location.replace("https://rintaroontachi.github.io/");
    } catch (e) {
      console.error("missing:", e);
    }
  }

  updateUI();
};

const updateUI = async () => {
  const isAuthenticated = await auth0Client.isAuthenticated();

  if (isAuthenticated) {
    const user = await auth0Client.getUser();
    document.getElementById("status").innerText = `${user.name}`;
    document.getElementById("btn-login").style.display = "none";
    document.getElementById("btn-logout").style.display = "block";
  } else {
    document.getElementById("status").innerText = "not yet log in";
    document.getElementById("btn-login").style.display = "block";
    document.getElementById("btn-logout").style.display = "none";
  }
};

const login = async () => {
  await auth0Client.loginWithRedirect();
};

const logout = () => {
  auth0Client.logout({
    logoutParams: {
      // 画像の設定「許可するログアウトURL」に合わせる
      returnTo: "https://rintaroontachi.github.io"
    }
  });
};
