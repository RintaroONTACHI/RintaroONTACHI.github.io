let auth0Client = null;

// Auth0の設定値
const config = {
  domain: "epsilon.jp.auth0.com", // Auth0ダッシュボードからコピー
  clientId: "TQ8auFHVhAe44FtxkoOhUPyWScIOXIMI"   // Auth0ダッシュボードからコピー
};

window.onload = async () => {
  // Auth0の初期化
  auth0Client = await createAuth0Client({
    domain: config.domain,
    clientId: config.clientId,
    authorizationParams: {
      redirect_uri: window.location.origin + window.location.pathname
    }
  });

  // ログイン後のリダイレクト処理
  const query = window.location.search;
  if (query.includes("code=") && query.includes("state=")) {
    try {
      await auth0Client.handleRedirectCallback();
      window.history.replaceState({}, document.title, window.location.pathname);
    } catch (err) {
      console.error("Login error:", err);
    }
  }

  // ログイン状態の確認
  const isAuthenticated = await auth0Client.isAuthenticated();

  if (isAuthenticated) {
    // ログイン済み：コンテンツを表示
    document.getElementById("loading-view").style.display = "none";
    document.getElementById("logged-in-view").style.display = "block";
    
    const user = await auth0Client.getUser();
    console.log("Logged in as:", user.name);
  } else {
    // 未ログイン：即座にAuth0ログイン画面へ飛ばす
    await auth0Client.loginWithRedirect();
  }
};

const logout = () => {
  auth0Client.logout({
    logoutParams: {
      returnTo: window.location.origin + window.location.pathname
    }
  });
};
