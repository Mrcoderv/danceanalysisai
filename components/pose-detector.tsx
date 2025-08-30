"use client"

import type React from "react"

import { useRef, useEffect, useState } from "react"
import { Button } from "@/components/ui/button"
import { Upload, Play, Pause, RotateCcw } from "lucide-react"

interface PoseDetectorProps {
  mode: "upload" | "camera"
  onPoseDetection: (poses: any[]) => void
  onAnalysisComplete: (data: any) => void
  danceStyle?: string // Added dance style prop
}

export function PoseDetector({ mode, onPoseDetection, onAnalysisComplete, danceStyle }: PoseDetectorProps) {
  const videoRef = useRef<HTMLVideoElement>(null)
  const canvasRef = useRef<HTMLCanvasElement>(null)
  const fileInputRef = useRef<HTMLInputElement>(null)
  const [isPlaying, setIsPlaying] = useState(false)
  const [isLoading, setIsLoading] = useState(false)
  const [stream, setStream] = useState<MediaStream | null>(null)

  const handleFileUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0]
    if (file) {
      const videoUrl = URL.createObjectURL(file)
      videoRef.current!.src = videoUrl
      videoRef.current!.load()
    }
  }

  const togglePlayback = () => {
    if (videoRef.current) {
      if (videoRef.current.paused || videoRef.current.ended) {
        videoRef.current.play()
        setIsPlaying(true)
      } else {
        videoRef.current.pause()
        setIsPlaying(false)
      }
    }
  }

  const resetVideo = () => {
    if (videoRef.current) {
      videoRef.current.currentTime = 0
    }
  }

  const startPoseDetection = () => {
    const detectPoses = () => {
      if (!isPlaying || !videoRef.current) return

      const time = Date.now() * 0.001
      const baseX = 320
      const baseY = 240

      // Simulate natural body movement with sine waves
      const bodySwayX = Math.sin(time * 2) * 20
      const armSwingY = Math.sin(time * 3) * 15
      const legMovementX = Math.cos(time * 1.5) * 10

      const mockPoses = [
        {
          keypoints: [
            { x: baseX + bodySwayX, y: baseY - 140, confidence: 0.9, name: "nose" },
            { x: baseX - 50 + bodySwayX, y: baseY - 90, confidence: 0.8, name: "left_shoulder" },
            { x: baseX + 50 + bodySwayX, y: baseY - 90, confidence: 0.8, name: "right_shoulder" },
            { x: baseX - 80 + bodySwayX, y: baseY - 40 + armSwingY, confidence: 0.7, name: "left_elbow" },
            { x: baseX + 80 + bodySwayX, y: baseY - 40 + armSwingY, confidence: 0.7, name: "right_elbow" },
            { x: baseX - 100 + bodySwayX, y: baseY + 10 + armSwingY, confidence: 0.6, name: "left_wrist" },
            { x: baseX + 100 + bodySwayX, y: baseY + 10 + armSwingY, confidence: 0.6, name: "right_wrist" },
            { x: baseX - 30 + bodySwayX, y: baseY + 40, confidence: 0.8, name: "left_hip" },
            { x: baseX + 30 + bodySwayX, y: baseY + 40, confidence: 0.8, name: "right_hip" },
            { x: baseX - 35 + legMovementX, y: baseY + 110, confidence: 0.7, name: "left_knee" },
            { x: baseX + 35 + legMovementX, y: baseY + 110, confidence: 0.7, name: "right_knee" },
            { x: baseX - 40 + legMovementX, y: baseY + 180, confidence: 0.6, name: "left_ankle" },
            { x: baseX + 40 + legMovementX, y: baseY + 180, confidence: 0.6, name: "right_ankle" },
          ],
        },
      ]

      onPoseDetection(mockPoses)

      // Continue detection
      if (isPlaying) {
        requestAnimationFrame(detectPoses)
      }
    }

    detectPoses()
  }

  useEffect(() => {
    if (mode === "camera") {
      setIsLoading(true)
      navigator.mediaDevices
        .getUserMedia({ video: true })
        .then((stream) => {
          setStream(stream)
          videoRef.current!.srcObject = stream
          videoRef.current!.play()
          setIsPlaying(true)
          setIsLoading(false)
        })
        .catch((error) => {
          console.error("Error accessing camera:", error)
          setIsLoading(false)
        })
    }
  }, [mode])

  return (
    <div className="space-y-4">
      {mode === "upload" && (
        <div className="space-y-4">
          <input ref={fileInputRef} type="file" accept="video/*" onChange={handleFileUpload} className="hidden" />
          <Button onClick={() => fileInputRef.current?.click()} className="w-full" variant="outline">
            <Upload className="w-4 h-4 mr-2" />
            Choose Video File
          </Button>
        </div>
      )}

      <div className="relative bg-black rounded-lg overflow-hidden">
        <video ref={videoRef} className="w-full h-64 object-cover" muted playsInline />
        <canvas ref={canvasRef} className="absolute top-0 left-0 w-full h-full pointer-events-none" />
      </div>

      <div className="flex gap-2 justify-center">
        <Button onClick={togglePlayback} size="sm">
          {isPlaying ? <Pause className="w-4 h-4" /> : <Play className="w-4 h-4" />}
        </Button>
        <Button onClick={resetVideo} size="sm" variant="outline">
          <RotateCcw className="w-4 h-4" />
        </Button>
      </div>

      {isLoading && <p className="text-center text-sm text-gray-600 dark:text-gray-400">Loading camera...</p>}
    </div>
  )
}
