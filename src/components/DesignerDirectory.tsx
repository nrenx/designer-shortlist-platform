
import React, { useState, useEffect } from 'react';
import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Dialog, DialogContent, DialogHeader, DialogTitle } from '@/components/ui/dialog';
import { toast } from '@/hooks/use-toast';
import { 
  Calendar,
  ImageIcon,
  MapPin,
  ArrowUpDown,
  Eye,
  EyeOff,
  FileText,
  Flag,
  Bookmark,
  BookmarkCheck,
  Star,
  Phone,
  X,
  Undo2
} from 'lucide-react';

interface Designer {
  id: number;
  name: string;
  rating: number;
  description: string;
  projects: number;
  experience: number;
  priceRange: string;
  phone1: string;
  phone2: string;
  location: string;
  specialties: string[];
  portfolio: string[];
}

interface SortOption {
  label: string;
  key: keyof Designer;
  order: 'asc' | 'desc';
}

const DesignerDirectory = () => {
  const [designers, setDesigners] = useState<Designer[]>([]);
  const [filteredDesigners, setFilteredDesigners] = useState<Designer[]>([]);
  const [shortlistedIds, setShortlistedIds] = useState<Set<number>>(new Set());
  const [hiddenIds, setHiddenIds] = useState<Set<number>>(new Set());
  const [showOnlyShortlisted, setShowOnlyShortlisted] = useState(false);
  const [showScheduleModal, setShowScheduleModal] = useState(false);
  const [showGalleryModal, setShowGalleryModal] = useState(false);
  const [showMapModal, setShowMapModal] = useState(false);
  const [showSortOptions, setShowSortOptions] = useState(false);
  const [showDetailsModal, setShowDetailsModal] = useState(false);
  const [showReportModal, setShowReportModal] = useState(false);
  const [selectedDesigner, setSelectedDesigner] = useState<Designer | null>(null);
  const [recentlyHidden, setRecentlyHidden] = useState<number | null>(null);
  const [currentSort, setCurrentSort] = useState<SortOption>({
    label: 'Sort by Experience',
    key: 'experience',
    order: 'desc'
  });

  const sortOptions: SortOption[] = [
    { label: 'Sort by Experience', key: 'experience', order: 'desc' },
    { label: 'Sort by Price', key: 'priceRange', order: 'asc' },
    { label: 'Sort by Projects', key: 'projects', order: 'desc' }
  ];

  useEffect(() => {
    loadDesigners();
  }, []);

  useEffect(() => {
    applyFilters();
  }, [designers, shortlistedIds, hiddenIds, showOnlyShortlisted, currentSort]);

  const loadDesigners = async () => {
    try {
      const response = await fetch('/src/data/listings.json');
      const data = await response.json();
      setDesigners(data);
    } catch (error) {
      console.error('Error loading designers:', error);
      // Fallback data if JSON loading fails
      setDesigners([]);
    }
  };

  const applyFilters = () => {
    let filtered = designers.filter(designer => !hiddenIds.has(designer.id));
    
    if (showOnlyShortlisted) {
      filtered = filtered.filter(designer => shortlistedIds.has(designer.id));
    }

    // Apply sorting
    filtered = [...filtered].sort((a, b) => {
      const aValue = a[currentSort.key];
      const bValue = b[currentSort.key];
      
      if (currentSort.key === 'priceRange') {
        const priceOrder = { '$': 1, '$$': 2, '$$$': 3 };
        const aPrice = priceOrder[aValue as keyof typeof priceOrder] || 0;
        const bPrice = priceOrder[bValue as keyof typeof priceOrder] || 0;
        return currentSort.order === 'asc' ? aPrice - bPrice : bPrice - aPrice;
      }
      
      if (typeof aValue === 'number' && typeof bValue === 'number') {
        return currentSort.order === 'asc' ? aValue - bValue : bValue - aValue;
      }
      
      return 0;
    });

    setFilteredDesigners(filtered);
  };

  const toggleShortlist = (designerId: number) => {
    const newShortlisted = new Set(shortlistedIds);
    if (newShortlisted.has(designerId)) {
      newShortlisted.delete(designerId);
    } else {
      newShortlisted.add(designerId);
    }
    setShortlistedIds(newShortlisted);
  };

  const hideDesigner = (designerId: number) => {
    const newHidden = new Set(hiddenIds);
    newHidden.add(designerId);
    setHiddenIds(newHidden);
    setRecentlyHidden(designerId);
    
    setTimeout(() => {
      if (recentlyHidden === designerId) {
        setRecentlyHidden(null);
      }
    }, 5000);
  };

  const undoHide = () => {
    if (recentlyHidden) {
      const newHidden = new Set(hiddenIds);
      newHidden.delete(recentlyHidden);
      setHiddenIds(newHidden);
      setRecentlyHidden(null);
    }
  };

  const handleSort = (sortOption: SortOption) => {
    setCurrentSort(sortOption);
    setShowSortOptions(false);
  };

  const renderStars = (rating: number) => {
    const stars = [];
    const fullStars = Math.floor(rating);
    const hasHalfStar = rating % 1 !== 0;

    for (let i = 0; i < fullStars; i++) {
      stars.push(<Star key={i} className="w-4 h-4 fill-yellow-400 text-yellow-400" />);
    }

    if (hasHalfStar) {
      stars.push(<Star key="half" className="w-4 h-4 fill-yellow-400/50 text-yellow-400" />);
    }

    const emptyStars = 5 - Math.ceil(rating);
    for (let i = 0; i < emptyStars; i++) {
      stars.push(<Star key={`empty-${i}`} className="w-4 h-4 text-gray-300" />);
    }

    return stars;
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-md mx-auto px-4 py-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <img 
              src="/lovable-uploads/de251bab-7a07-4dd1-ab51-268854eca36e.png" 
              alt="EmptyCup" 
              className="w-8 h-8"
            />
            <h1 className="text-xl font-semibold text-gray-900">EmptyCup</h1>
          </div>
          <Button variant="ghost" size="sm">
            <div className="w-6 h-6 grid grid-cols-3 gap-0.5">
              {[...Array(9)].map((_, i) => (
                <div key={i} className="w-1 h-1 bg-gray-600 rounded-full" />
              ))}
            </div>
          </Button>
        </div>
      </header>

      {/* Navigation Tabs */}
      <div className="bg-white border-b">
        <div className="max-w-md mx-auto px-4">
          <div className="flex justify-between py-3">
            <Button
              variant="ghost"
              size="sm"
              onClick={() => setShowScheduleModal(true)}
              className="flex flex-col items-center gap-1 h-auto py-2 text-amber-600"
            >
              <Calendar className="w-5 h-5" />
              <span className="text-xs">Schedule</span>
            </Button>
            
            <Button
              variant="ghost"
              size="sm"
              onClick={() => setShowGalleryModal(true)}
              className="flex flex-col items-center gap-1 h-auto py-2"
            >
              <ImageIcon className="w-5 h-5" />
              <span className="text-xs">Gallery</span>
            </Button>
            
            <Button
              variant="ghost"
              size="sm"
              onClick={() => setShowMapModal(true)}
              className="flex flex-col items-center gap-1 h-auto py-2"
            >
              <MapPin className="w-5 h-5" />
              <span className="text-xs">Map</span>
            </Button>
            
            <Button
              variant="ghost"
              size="sm"
              onClick={() => setShowOnlyShortlisted(!showOnlyShortlisted)}
              className={`flex flex-col items-center gap-1 h-auto py-2 ${showOnlyShortlisted ? 'text-blue-600' : ''}`}
            >
              <Bookmark className="w-5 h-5" />
              <span className="text-xs">Shortlisted</span>
            </Button>
            
            <Button
              variant="ghost"
              size="sm"
              onClick={() => setShowSortOptions(!showSortOptions)}
              className="flex flex-col items-center gap-1 h-auto py-2"
            >
              <ArrowUpDown className="w-5 h-5" />
              <span className="text-xs">Sort</span>
            </Button>
          </div>
        </div>
      </div>

      {/* Sort Options Dropdown */}
      {showSortOptions && (
        <div className="bg-white border-b shadow-sm">
          <div className="max-w-md mx-auto px-4 py-2">
            {sortOptions.map((option) => (
              <Button
                key={option.label}
                variant="ghost"
                size="sm"
                onClick={() => handleSort(option)}
                className={`w-full justify-start ${currentSort.label === option.label ? 'bg-blue-50 text-blue-600' : ''}`}
              >
                {option.label}
              </Button>
            ))}
          </div>
        </div>
      )}

      {/* Designer Cards */}
      <div className="max-w-md mx-auto px-4 py-6 space-y-4">
        {filteredDesigners.map((designer) => (
          <Card key={designer.id} className="p-4 bg-white shadow-sm">
            <div className="flex justify-between items-start mb-3">
              <div>
                <h3 className="text-lg font-semibold text-gray-900">{designer.name}</h3>
                <div className="flex items-center gap-1 mt-1">
                  {renderStars(designer.rating)}
                </div>
              </div>
              <Button
                variant="ghost"
                size="sm"
                onClick={() => {
                  setSelectedDesigner(designer);
                  setShowDetailsModal(true);
                }}
                className="text-amber-600 text-sm"
              >
                Details
              </Button>
            </div>

            <p className="text-gray-600 text-sm mb-4">{designer.description}</p>

            <div className="grid grid-cols-3 gap-4 mb-4">
              <div className="text-center">
                <div className="text-xl font-bold text-gray-900">{designer.projects}</div>
                <div className="text-xs text-gray-500">Projects</div>
              </div>
              <div className="text-center">
                <div className="text-xl font-bold text-gray-900">{designer.experience}</div>
                <div className="text-xs text-gray-500">Years</div>
              </div>
              <div className="text-center">
                <div className="text-xl font-bold text-gray-900">{designer.priceRange}</div>
                <div className="text-xs text-gray-500">Price</div>
              </div>
            </div>

            <div className="space-y-1 mb-4">
              <div className="text-sm text-gray-700">{designer.phone1}</div>
              <div className="text-sm text-gray-700">{designer.phone2}</div>
            </div>

            <div className="flex justify-between items-center">
              <div className="flex gap-2">
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={() => hideDesigner(designer.id)}
                  className="text-gray-500"
                >
                  <EyeOff className="w-4 h-4" />
                  <span className="ml-1 text-xs">Hide</span>
                </Button>
                
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={() => {
                    setSelectedDesigner(designer);
                    setShowReportModal(true);
                  }}
                  className="text-gray-500"
                >
                  <Flag className="w-4 h-4" />
                  <span className="ml-1 text-xs">Report</span>
                </Button>
              </div>

              <Button
                variant="ghost"
                size="sm"
                onClick={() => toggleShortlist(designer.id)}
                className={shortlistedIds.has(designer.id) ? 'text-red-500' : 'text-gray-400'}
              >
                {shortlistedIds.has(designer.id) ? (
                  <BookmarkCheck className="w-5 h-5 fill-current" />
                ) : (
                  <Bookmark className="w-5 h-5" />
                )}
                <span className="ml-1 text-xs">Shortlist</span>
              </Button>
            </div>
          </Card>
        ))}

        {filteredDesigners.length === 0 && (
          <div className="text-center py-8">
            <p className="text-gray-500">No designers found</p>
          </div>
        )}
      </div>

      {/* Undo Snackbar */}
      {recentlyHidden && (
        <div className="fixed bottom-4 left-4 right-4 max-w-md mx-auto">
          <div className="bg-gray-800 text-white rounded-lg p-4 flex items-center justify-between">
            <span className="text-sm">Designer hidden</span>
            <Button
              variant="ghost"
              size="sm"
              onClick={undoHide}
              className="text-white hover:text-gray-200"
            >
              <Undo2 className="w-4 h-4 mr-1" />
              Undo
            </Button>
          </div>
        </div>
      )}

      {/* Schedule Modal */}
      <Dialog open={showScheduleModal} onOpenChange={setShowScheduleModal}>
        <DialogContent className="max-w-sm">
          <DialogHeader>
            <DialogTitle>Schedule Appointment</DialogTitle>
          </DialogHeader>
          <div className="text-center py-8">
            <Calendar className="w-16 h-16 mx-auto text-gray-300 mb-4" />
            <p className="text-gray-600">Booking functionality coming soon. Stay tuned!</p>
          </div>
        </DialogContent>
      </Dialog>

      {/* Gallery Modal */}
      <Dialog open={showGalleryModal} onOpenChange={setShowGalleryModal}>
        <DialogContent className="max-w-sm">
          <DialogHeader>
            <DialogTitle>Sample Portfolio</DialogTitle>
          </DialogHeader>
          <div className="grid grid-cols-2 gap-2">
            {[
              "https://images.unsplash.com/photo-1586023492125-27b2c045efd7?w=400",
              "https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?w=400",
              "https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?w=400",
              "https://images.unsplash.com/photo-1618221195710-dd6b41faaea8?w=400"
            ].map((img, idx) => (
              <img
                key={idx}
                src={img}
                alt={`Portfolio ${idx + 1}`}
                className="w-full h-24 object-cover rounded"
              />
            ))}
          </div>
        </DialogContent>
      </Dialog>

      {/* Map Modal */}
      <Dialog open={showMapModal} onOpenChange={setShowMapModal}>
        <DialogContent className="max-w-sm">
          <DialogHeader>
            <DialogTitle>Designer Locations</DialogTitle>
          </DialogHeader>
          <div className="text-center py-8">
            <MapPin className="w-16 h-16 mx-auto text-gray-300 mb-4" />
            <p className="text-gray-600">Location services are currently disabled. Enable them to view designer locations.</p>
          </div>
        </DialogContent>
      </Dialog>

      {/* Details Modal */}
      <Dialog open={showDetailsModal} onOpenChange={setShowDetailsModal}>
        <DialogContent className="max-w-sm">
          <DialogHeader>
            <DialogTitle>{selectedDesigner?.name}</DialogTitle>
          </DialogHeader>
          {selectedDesigner && (
            <div className="space-y-4">
              <div className="flex items-center gap-1">
                {renderStars(selectedDesigner.rating)}
                <span className="ml-2 text-sm text-gray-600">{selectedDesigner.rating}/5</span>
              </div>
              
              <p className="text-gray-700">{selectedDesigner.description}</p>
              
              <div className="grid grid-cols-3 gap-4 py-4 border-y">
                <div className="text-center">
                  <div className="text-lg font-bold">{selectedDesigner.projects}</div>
                  <div className="text-xs text-gray-500">Projects</div>
                </div>
                <div className="text-center">
                  <div className="text-lg font-bold">{selectedDesigner.experience}</div>
                  <div className="text-xs text-gray-500">Years</div>
                </div>
                <div className="text-center">
                  <div className="text-lg font-bold">{selectedDesigner.priceRange}</div>
                  <div className="text-xs text-gray-500">Price</div>
                </div>
              </div>

              <div>
                <h4 className="font-medium mb-2">Contact Information</h4>
                <div className="space-y-1">
                  <div className="flex items-center gap-2">
                    <Phone className="w-4 h-4 text-gray-400" />
                    <span className="text-sm">{selectedDesigner.phone1}</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <Phone className="w-4 h-4 text-gray-400" />
                    <span className="text-sm">{selectedDesigner.phone2}</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <MapPin className="w-4 h-4 text-gray-400" />
                    <span className="text-sm">{selectedDesigner.location}</span>
                  </div>
                </div>
              </div>

              <div>
                <h4 className="font-medium mb-2">Specialties</h4>
                <div className="flex flex-wrap gap-1">
                  {selectedDesigner.specialties.map((specialty) => (
                    <Badge key={specialty} variant="secondary" className="text-xs">
                      {specialty}
                    </Badge>
                  ))}
                </div>
              </div>
            </div>
          )}
        </DialogContent>
      </Dialog>

      {/* Report Modal */}
      <Dialog open={showReportModal} onOpenChange={setShowReportModal}>
        <DialogContent className="max-w-sm">
          <DialogHeader>
            <DialogTitle>Report Designer</DialogTitle>
          </DialogHeader>
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium mb-2">Reason for report</label>
              <select className="w-full p-2 border rounded-md">
                <option>Inappropriate content</option>
                <option>Fake profile</option>
                <option>Spam</option>
                <option>Other</option>
              </select>
            </div>
            
            <div>
              <label className="block text-sm font-medium mb-2">Describe the issue</label>
              <textarea 
                className="w-full p-2 border rounded-md h-20 resize-none"
                placeholder="Please provide more details..."
              />
            </div>
            
            <Button 
              className="w-full"
              onClick={() => {
                setShowReportModal(false);
                toast({
                  title: "Report submitted",
                  description: "Thank you for your feedback. We'll review this report.",
                });
              }}
            >
              Submit Report
            </Button>
          </div>
        </DialogContent>
      </Dialog>
    </div>
  );
};

export default DesignerDirectory;
