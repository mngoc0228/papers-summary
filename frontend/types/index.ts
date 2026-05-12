export  interface IPaper {
  id: string;
  title: string;
  abstract: string;
  authors: string[];
  published_date: string;
  url: string;
  summary: string;
  topics: ITopic[];
}

export interface ITopic {
  id: string;
  name: string;
  code: string;
  description: string;
}