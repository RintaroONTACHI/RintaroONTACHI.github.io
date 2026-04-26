let auth0Client = null;

// Auth0の設定値
const config = {
  domain: "epsilon.jp.auth0.com", // Auth0ダッシュボードからコピー
  clientId: "TQ8auFHVhAe44FtxkoOhUPyWScIOXIMI"   // Auth0ダッシュボードからコピー
};

window.onload = async () => {
  // 1. Initialize Auth0 Client
  auth0Client = await createAuth0Client({
    domain: config.domain,
    clientId: config.clientId,
    authorizationParams: {
      redirect_uri: window.location.origin + window.location.pathname
    }
  });

  // 2. Handle the redirect from Auth0
  const query = window.location.search;
  if (query.includes("code=") && query.includes("state=")) {
    try {
      await auth0Client.handleRedirectCallback();
      window.history.replaceState({}, document.title, window.location.pathname);
    } catch (err) {
      console.error("Login error:", err);
    }
  }

  // 3. Check authentication status
  const isAuthenticated = await auth0Client.isAuthenticated();

  if (isAuthenticated) {
    // Show members-only content
    showApp();
  } else {
    // If not logged in, redirect to login page immediately
    login();
  }
};

const showApp = async () => {
  const user = await auth0Client.getUser();
  
  // Update UI for members
  document.getElementById("status").innerText = `Welcome, ${user.name}!`;
  document.getElementById("logged-in-view").style.display = "block";
  document.getElementById("loading-view").style.display = "none";
};

// Execute Login
const login = async () => {
  await auth0Client.loginWithRedirect();
};

// Execute Logout
const logout = () => {
  auth0Client.logout({
    logoutParams: {
      returnTo: window.location.origin + window.location.pathname
    }
  });
};
