declare module 'react' {
  import * as React from 'react';
  export = React;
  export as namespace React;
}

declare module 'react-router-dom' {
  export interface NavigateFunction {
    (to: string, options?: { replace?: boolean; state?: any }): void;
  }

  export interface Location {
    pathname: string;
    search: string;
    hash: string;
    state: any;
  }

  export interface NavigateProps {
    to: string;
    replace?: boolean;
    state?: any;
  }

  export function useNavigate(): NavigateFunction;
  export function useLocation(): Location;
  export function Link(props: { to: string; className?: string; children: React.ReactNode }): JSX.Element;
  export function Navigate(props: NavigateProps): JSX.Element;
  export function BrowserRouter(props: { children: React.ReactNode }): JSX.Element;
  export function Routes(props: { children: React.ReactNode }): JSX.Element;
  export function Route(props: { path: string; element: React.ReactNode }): JSX.Element;
}

declare module 'axios' {
  interface AxiosRequestConfig {
    url?: string;
    method?: string;
    baseURL?: string;
    headers?: any;
    params?: any;
    data?: any;
    timeout?: number;
    withCredentials?: boolean;
  }

  interface AxiosResponse<T = any> {
    data: T;
    status: number;
    statusText: string;
    headers: any;
    config: AxiosRequestConfig;
  }

  interface AxiosError<T = any> extends Error {
    config: AxiosRequestConfig;
    code?: string;
    request?: any;
    response?: AxiosResponse<T>;
  }

  interface AxiosInstance {
    defaults: AxiosRequestConfig;
    get<T = any>(url: string, config?: AxiosRequestConfig): Promise<AxiosResponse<T>>;
    post<T = any>(url: string, data?: any, config?: AxiosRequestConfig): Promise<AxiosResponse<T>>;
    put<T = any>(url: string, data?: any, config?: AxiosRequestConfig): Promise<AxiosResponse<T>>;
    delete<T = any>(url: string, config?: AxiosRequestConfig): Promise<AxiosResponse<T>>;
  }

  const axios: AxiosInstance;
  export default axios;
} 