let auth0Client = null;

// Auth0の設定値
const config = {
  domain: "YOUR_AUTH0_DOMAIN", // Auth0ダッシュボードからコピー
  clientId: "YOUR_CLIENT_ID"   // Auth0ダッシュボードからコピー
};

window.onload = async () => {
  // 1. Auth0クライアントの初期化
  auth0Client = await createAuth0Client({
    domain: config.domain,
    clientId: config.clientId,
    authorizationParams: {
      // 設定を削ったので、トップページを指定
      redirect_uri: window.location.origin + window.location.pathname
    }
  });

  // 2. ログイン後の処理（Auth0から戻ってきた時）
  const query = window.location.search;
  if (query.includes("code=") && query.includes("state=")) {
    try {
      await auth0Client.handleRedirectCallback();
      // URLをきれいにする
      window.history.replaceState({}, document.title, window.location.pathname);
    } catch (err) {
      console.error("error:", err);
    }
  }

  // 3. ログイン状態に応じて画面を更新
  updateUI();
};

const updateUI = async () => {
  const isAuthenticated = await auth0Client.isAuthenticated();

  const loggedInView = document.getElementById("logged-in-view");
  const loggedOutView = document.getElementById("logged-out-view");
  const statusText = document.getElementById("status");

  if (isAuthenticated) {
    // ログイン済み：秘密のページを表示
    const user = await auth0Client.getUser();
    statusText.innerText = `${user.name} ,Hello!`;
    loggedInView.style.display = "block";
    loggedOutView.style.display = "none";
  } else {
    // 未ログイン：ログイン案内を表示
    statusText.innerText = "it can be accessed everyone.";
    loggedInView.style.display = "none";
    loggedOutView.style.display = "block";
  }
};

// ログイン実行
const login = async () => {
  await auth0Client.loginWithRedirect();
};

// ログアウト実行
const logout = () => {
  auth0Client.logout({
    logoutParams: {
      returnTo: window.location.origin + window.location.pathname
    }
  });
};
