import { API_BASE_URL } from "./config";

const apiOrigin = API_BASE_URL.startsWith("http")
  ? new URL(API_BASE_URL).origin
  : "";

export const resolveMediaUrl = (path) => {
  if (!path || path.startsWith("http://") || path.startsWith("https://")) {
    return path;
  }
  return `${apiOrigin}${path.startsWith("/") ? path : `/${path}`}`;
};

export const installMediaCssVariables = () => {
  const mediaRoot = `${apiOrigin}/api/media/app-assets`;
  const assets = {
    "--image-restaurant-table": "restaurant-table.jpeg",
    "--image-menu-table": "menu-table.jpeg",
    "--image-dining-room": "dining-room.jpeg",
    "--image-login-dining": "login-dining.jpeg",
    "--image-register-dining": "register-dining.jpeg",
    "--image-customer-dining": "customer-dining.jpeg",
    "--image-restaurant-details": "restaurant-details.jpeg",
  };

  Object.entries(assets).forEach(([variable, filename]) => {
    document.documentElement.style.setProperty(
      variable,
      `url("${mediaRoot}/${filename}")`
    );
  });
};
