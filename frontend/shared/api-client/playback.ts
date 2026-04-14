import { apiClient } from './client'
import type { PlaybackState } from '../../types/playback'

export async function fetchPlaybackState(): Promise<PlaybackState> {
  const resp = await apiClient.get('/playback/state')
  return resp.data?.data ?? resp.data
}
