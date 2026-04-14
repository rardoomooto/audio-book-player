export interface ContentItem {
  id: string
  title: string
  duration?: number
  author?: string
  coverUrl?: string
}

export type ContentList = ContentItem[]
